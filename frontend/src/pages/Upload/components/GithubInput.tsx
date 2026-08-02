import { Input } from "@/components/ui/input";

function GithubInput() {
    return (
        <div className="space-y-2">
            <label className="font-medium">
                GitHub Repository URL
            </label>

            <Input
                placeholder="https://github.com/username/repository"
            />
        </div>
    );
}

export default GithubInput;