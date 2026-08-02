import { Button } from "@/components/ui/button";

function QuickActions() {
    return (
        <div className="flex flex-wrap gap-4">
            <Button>
                Generate Docs
            </Button>

            <Button variant="outline">
                Architecture
            </Button>

            <Button variant="outline">
                Knowledge Base
            </Button>

            <Button variant="outline">
                Ask AI
            </Button>
        </div>
    );
}

export default QuickActions;