import { recentRepositories } from "../uploadData";

function RecentUploads() {
    return (
        <div className="rounded-xl border p-6">
            <h2 className="mb-4 text-lg font-semibold">
                Recent Uploads
            </h2>

            <div className="space-y-3">
                {recentRepositories.map((repo) => (
                    <div
                        key={repo.id}
                        className="rounded-lg border p-3"
                    >
                        {repo.name}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default RecentUploads;