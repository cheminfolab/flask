import Layout from "@/components/layout"
import SubstanceSidebar from "@/components/substances-sidebar"

const Substances = () => (
    <Layout
        auxSidebar={<SubstanceSidebar />}
        children={
            <div className="flex flex-1 flex-col gap-4 p-4">
                {Array.from({ length: 24 }).map((_, index) => (
                    <div
                        key={index}
                        className="bg-muted/50 aspect-video h-12 w-full rounded-lg"
                    />
                ))}
            </div>
        } 
    />
)

export default Substances