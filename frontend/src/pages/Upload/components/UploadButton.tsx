import { Button } from "@/components/ui/button";

interface UploadButtonProps {
    disabled: boolean;
    onClick: () => void;
}

function UploadButton({
    disabled,
    onClick,
}: UploadButtonProps) {
    return (
        <Button
            className="w-full"
            disabled={disabled}
            onClick={onClick}
        >
            Analyze Repository
        </Button>
    );
}

export default UploadButton;