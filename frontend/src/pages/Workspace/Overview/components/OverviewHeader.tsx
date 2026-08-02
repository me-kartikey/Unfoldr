import { Upload } from "lucide-react";
import { Button } from "@/components/ui/button";

function OverviewHeader() {
    return (
        <div className="flex items-center justify-between">
            <div>
                <h1 className="text-3xl font-bold">
                    Repository Overview
                </h1>

                <p className="mt-2 text-muted-foreground">
                    AI-powered insights into your repository.
                </p>
            </div>

            <Button>
                <Upload className="mr-2 h-4 w-4" />
                Upload Repository
            </Button>
        </div>
    );
}

export default OverviewHeader;