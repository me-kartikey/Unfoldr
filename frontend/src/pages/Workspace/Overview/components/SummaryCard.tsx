interface SummaryCardProps {
    summary: string;
}

function SummaryCard({
    summary,
}: SummaryCardProps) {
    return (
        <div className="rounded-xl border bg-white p-6 shadow-sm">
            <h2 className="mb-3 text-lg font-semibold">
                AI Repository Summary
            </h2>

            <p className="leading-7 text-slate-600">
                {summary}
            </p>
        </div>
    );
}

export default SummaryCard;