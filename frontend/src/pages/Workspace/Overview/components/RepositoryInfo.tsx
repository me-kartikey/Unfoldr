interface RepositoryInfoProps {
    repository: string;
    branch: string;
    backend: string;
    status: string;
    lastAnalyzed: string;
}

function RepositoryInfo({
    repository,
    branch,
    backend,
    status,
    lastAnalyzed,
}: RepositoryInfoProps) {
    return (
        <div className="rounded-xl border bg-white p-6 shadow-sm">
            <h2 className="mb-5 text-lg font-semibold">
                Repository Information
            </h2>

            <div className="grid grid-cols-2 gap-6">
                <div>
                    <p className="text-sm text-slate-500">Repository</p>
                    <p className="font-medium">{repository}</p>
                </div>

                <div>
                    <p className="text-sm text-slate-500">Branch</p>
                    <p className="font-medium">{branch}</p>
                </div>

                <div>
                    <p className="text-sm text-slate-500">Backend</p>
                    <p className="font-medium">{backend}</p>
                </div>

                <div>
                    <p className="text-sm text-slate-500">Status</p>
                    <p className="font-medium">{status}</p>
                </div>

                <div>
                    <p className="text-sm text-slate-500">Last Analyzed</p>
                    <p className="font-medium">{lastAnalyzed}</p>
                </div>
            </div>
        </div>
    );
}

export default RepositoryInfo;