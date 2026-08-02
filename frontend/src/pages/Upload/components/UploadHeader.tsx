function UploadHeader() {
    return (
        <div>
            <h1 className="text-3xl font-bold">
                Upload Repository
            </h1>

            <p className="mt-2 text-muted-foreground">
                Upload a local repository or enter a GitHub URL to start AI analysis.
            </p>
        </div>
    );
}

export default UploadHeader;