import {
    GithubInput,
    RecentUploads,
    UploadButton,
    UploadDropzone,
    UploadHeader,
} from "./components";

function Upload() {
    return (
        <div className="mx-auto max-w-5xl space-y-8">
            <UploadHeader />

            <UploadDropzone />

            <GithubInput />

            <UploadButton />

            <RecentUploads />
        </div>
    );
}

export default Upload;