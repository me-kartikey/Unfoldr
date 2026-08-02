import { useRef } from "react";
import { UploadCloud } from "lucide-react";

function UploadDropzone() {
    // React remembers our hidden file input
    const inputRef = useRef<HTMLInputElement>(null);

    // Runs when the user clicks the upload box
    const handleClick = () => {
        inputRef.current?.click();
    };

    return (
        <>
            <div
                onClick={handleClick}
                className="flex h-64 cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed"
            >
                <UploadCloud className="mb-4 h-10 w-10" />

                <h3 className="text-lg font-semibold">
                    Drag & Drop Repository
                </h3>

                <p className="mt-2 text-sm text-muted-foreground">
                    or browse your local folder
                </p>
            </div>

            <input
                ref={inputRef}
                type="file"
                hidden
            />
        </>
    );
}

export default UploadDropzone;