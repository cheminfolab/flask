import type { ReactNode } from "react"

export interface BreadcrumbItemLink {
    name: string
    link: string
}

export interface LayoutProps {
    children: ReactNode
    auxSidebar?: ReactNode
    header?: ReactNode
}

export type LayoutType = (props: LayoutProps) => ReactNode
