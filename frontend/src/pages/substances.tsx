import { useEffect, useState } from "react"
import {
    Breadcrumb,
    BreadcrumbList,
} from "@/components/ui/breadcrumb"
import {
    SidebarTrigger,
} from "@/components/ui/sidebar"
import { Separator } from "@/components/ui/separator"
import { SearchForm } from "@/components/search-form"

import type { ColumnDef } from "@tanstack/react-table"

import useAxios from "@/hooks/useAxios"
import { errorMessage } from "@/lib/api"
import Layout, { Breadcrumbs } from "@/components/layout"
import { DataTable } from "@/components/substance-table"
import FormulaFormatter from "@/components/FormulaFormatter"
import type { Substance } from "@/types/api"

const columns: ColumnDef<Substance>[] = [
    { accessorKey: "name", header: "Name" },
    { accessorKey: "label", header: "Label" },
    {
        accessorKey: "formula",
        header: "Formula",
        cell: ({ row }) => row.original.formula
            ? <FormulaFormatter formula={row.original.formula} />
            : null,
    },
    { accessorKey: "cas", header: "CAS" },
    { accessorKey: "mol_weight", header: "Molar mass" },
]

const SubstanceHeader = () => (
    <header className="sticky top-0 flex shrink-0 items-center gap-2 px-4 h-16 border-b bg-background w-full">
        <SidebarTrigger />
        <Separator
            orientation="vertical"
            className="mr-2 h-4"
        />
        <Breadcrumb>
        <BreadcrumbList>
            <Breadcrumbs items={[
                {name: "Home", link: "/"},
                {name: "Substances", link: "/substances"},
            ]} />
        </BreadcrumbList>
        </Breadcrumb>
        <SearchForm className="w-full sm:ml-auto sm:w-auto" />
    </header>
)

const Substances = () => {
    const [substances, setSubstances] = useState<Substance[]>([])
    const [error, setError] = useState<string | null>(null)
    const api = useAxios()

    useEffect(() => {
        api
            .getAll<Substance[]>("substances")
            .then(data => setSubstances(data))
            .catch(error => setError(errorMessage(error)))
    }, [api])

    return(
        <Layout
            header={<SubstanceHeader />}
            children={
                <div className="flex flex-1 flex-col gap-4 p-4">
                    {error ? <p role="alert" className="text-destructive text-sm">{error}</p> : null}
                    <DataTable columns={columns} data={substances} />
                </div>
            }
        />
    )
}

export default Substances