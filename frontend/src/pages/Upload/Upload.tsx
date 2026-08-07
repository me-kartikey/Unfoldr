import { useState } from "react";

import {
    GithubInput,
    RecentUploads,
    UploadButton,
    UploadDropzone,
    UploadHeader,
} from "./components";

import { uploadRepository } from "@/services/repositoryService";

function Upload() {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [isUploading, setIsUploading] = useState(false);

    const handleAnalyzeRepository = async () => {
        if (!selectedFile) return;

        try {
            setIsUploading(true);

            const repository = await uploadRepository(selectedFile);

            console.log("Repository Uploaded Successfully");
            console.log(repository);

        } catch (error) {
            console.error("Upload Failed:", error);
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <div className="mx-auto max-w-5xl space-y-8">
            <UploadHeader />

            <UploadDropzone
                selectedFile={selectedFile}
                setSelectedFile={setSelectedFile}
            />

            <GithubInput />

            <UploadButton
                disabled={!selectedFile || isUploading}
                onClick={handleAnalyzeRepository}
            />

            <RecentUploads />
        </div>
    );
}

export default Upload;