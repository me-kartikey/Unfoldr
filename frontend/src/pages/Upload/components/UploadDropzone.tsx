import { UploadCloud } from "lucide-react";
import {useRef} from "react";
interface UploadDropzoneProps {
    selectedFile: File | null;
    setSelectedFile: React.Dispatch<
        React.SetStateAction<File | null>
    >;
}
function UploadDropzone({
    selectedFile,
    setSelectedFile,
}: UploadDropzoneProps) {
    // Reference to the hidden file input
    const inputRef = useRef<HTMLInputElement>(null);

    // Opens the hidden file input
    const handleClick = () => {
        inputRef.current?.click();
    };

    // Runs when the user selects a file
    const handleFileChange = (
        event: React.ChangeEvent<HTMLInputElement>
    ) => {
        const file = event.target.files?.[0];

        if (!file) return;

        setSelectedFile(file);
    };

    return (
        <>
            <div
                onClick={handleClick}
                className="flex h-64 cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-slate-300 transition-colors hover:border-slate-500"
            >
                <UploadCloud className="mb-4 h-10 w-10 text-slate-500" />

                <h3 className="text-lg font-semibold">
                    {selectedFile
                        ? selectedFile.name
                        : "Drag & Drop Repository"}
                </h3>

                <p className="mt-2 text-sm text-muted-foreground">
                    {selectedFile
                        ? "Repository selected successfully"
                        : "or browse your local folder"}
                </p>
            </div>

            <input
                ref={inputRef}
                type="file"
                hidden
                onChange={handleFileChange}
            />
        </>
    );
}

export default UploadDropzone;