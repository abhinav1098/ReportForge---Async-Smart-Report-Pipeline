import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "./lib/api";

function getDisplayStatus(report: any) {
  if (report.status === "processing" && report.retry_count > 0) {
    return "retrying";
  }
  return report.status;
}

function getStatusColor(status: string) {
  switch (status) {
    case "pending":
      return "#f59e0b";
    case "processing":
      return "#3b82f6";
    case "retrying":
      return "#f97316";
    case "completed":
      return "#10b981";
    case "failed":
      return "#ef4444";
    default:
      return "#6b7280";
  }
}

function getStatusIcon(status: string) {
  switch (status) {
    case "pending":
      return "⏳";
    case "processing":
      return "⚙️";
    case "retrying":
      return "🔁";
    case "completed":
      return "✅";
    case "failed":
      return "❌";
    default:
      return "•";
  }
}

function App() {
  const queryClient = useQueryClient();
  const [deletingId, setDeletingId] = useState<number | null>(null);

  // ⭐ IMPORTANT: disable polling while deleting
  const { data: reports, isLoading } = useQuery({
    queryKey: ["reports"],
    queryFn: async () => {
      const res = await api.get("/reports");
      return res.data;
    },
    refetchInterval: deletingId ? false : 3000,
  });

  const createMutation = useMutation({
    mutationFn: async () => {
      await api.post("/reports", {
        title: "Generated from UI",
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["reports"] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      await api.delete(`/reports/${id}`);
    },

    // ⭐ true optimistic update
    onMutate: async (id: number) => {
      setDeletingId(id);

      await queryClient.cancelQueries({ queryKey: ["reports"] });

      const previousReports = queryClient.getQueryData<any[]>(["reports"]);

      queryClient.setQueryData<any[]>(["reports"], (old) =>
        old?.filter((r) => r.id !== id) ?? []
      );

      return { previousReports };
    },

    onError: (_err, _id, context) => {
      if (context?.previousReports) {
        queryClient.setQueryData(["reports"], context.previousReports);
      }
    },

    onSettled: () => {
      setDeletingId(null);
      queryClient.invalidateQueries({ queryKey: ["reports"] });
    },
  });

  return (
    <div className="container">
      <h1>🚀 Smart Report Generator</h1>

      <button
        className="generate-btn"
        disabled={createMutation.isPending}
        onClick={() => createMutation.mutate()}
      >
        {createMutation.isPending ? "Generating..." : "Generate Report"}
      </button>

      <h2>Reports</h2>

      {isLoading ? (
        <p>Loading reports...</p>
      ) : (
        <ul className="report-list">
          {reports?.map((r: any) => {
            const displayStatus = getDisplayStatus(r);

            return (
              <li key={r.id} className="report-item">
                <span>
                  <strong>#{r.id}</strong> — {r.title}
                </span>

                <div className="right-section">
                  <span
                    className="status-badge"
                    style={{
                      backgroundColor: getStatusColor(displayStatus),
                    }}
                  >
                    {getStatusIcon(displayStatus)} {displayStatus}
                  </span>

                  <button
                    className="delete-btn"
                    disabled={deletingId === r.id}
                    onClick={() => {
                      if (!confirm("Delete this report?")) return;
                      deleteMutation.mutate(r.id);
                    }}
                  >
                    {deletingId === r.id ? "Deleting..." : "🗑️"}
                  </button>
                </div>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}

export default App;
