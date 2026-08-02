import OverviewHeader from "./components/OverviewHeader";
import StatCard from "./components/StatCard";
import SummaryCard from "./components/SummaryCard";
import QuickActions from "./components/QuickActions";
import {
    repositoryData,
    repositoryInfo,
    stats,
} from "./overviewData";
import RepositoryInfo from "./components/RepositoryInfo";

function Overview() {
    return (
        <div className="space-y-8">
            <OverviewHeader />

            <div className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-4">
                {stats.map((item) => (
                    <StatCard
                        key={item.title}
                        title={item.title}
                        value={item.value}
                        icon={item.icon}
                    />
                ))}
            </div>
            <RepositoryInfo
    repository={repositoryInfo.repository}
    branch={repositoryInfo.branch}
    backend={repositoryInfo.backend}
    status={repositoryInfo.status}
    lastAnalyzed={repositoryInfo.lastAnalyzed}
/>

            <SummaryCard summary={repositoryData.summary} />

            <QuickActions />
        </div>
    );
}

export default Overview;