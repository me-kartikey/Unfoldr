interface StatCardProps {
    title: string;
    value: string;
    icon: React.ElementType;
}

function StatCard({
    title,
    value,
    icon: Icon,
}: StatCardProps) {
    return (
        <div className="rounded-xl border bg-white p-5 shadow-sm">
            <div className="mb-4 flex items-center justify-between">
                <h3 className="text-sm text-slate-500">
                    {title}
                </h3>

                <Icon className="h-5 w-5 text-slate-500" />
            </div>

            <p className="text-2xl font-semibold">
                {value}
            </p>
        </div>
    );
}

export default StatCard;