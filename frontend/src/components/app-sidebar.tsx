import { useState, type ComponentProps } from "react"
import { Link, Outlet } from "react-router"
import { 
  Calendar, 
  Home, 
  Inbox,
  Settings,
  FolderOpen,
  PillBottle,
  ChartColumn,
  Cpu,
  Bolt,
  FlaskRound,
  CircleQuestionMark,
  ChevronsLeftRightEllipsis,
  BookMarked,
  type LucideIcon
} from "lucide-react"

import {
  Sidebar,
  SidebarHeader,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  // SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"

import { NavUser } from "./nav-user"
 
export const AppSidebar = ({...props}: ComponentProps<typeof Sidebar>) => {
  type ItemType = {
      title: string,
      url: string,
      icon: LucideIcon,
  }

  // Menu items.
  const items: ItemType[] = [
    {
      title: "Home",
      url: "/",
      icon: Home,
    },
    {
      title: "Projects",
      url: "/projects",
      icon: FolderOpen,
    },
    {
      title: "Substances",
      url: "/substances",
      icon: Bolt,
    },
    {
      title: "Containers",
      url: "/containers",
      icon: PillBottle,
    },
    {
      title: "Analytics",
      url: "#",
      icon: ChartColumn,
    },
    {
      title: "Calculations",
      url: "#",
      icon: Cpu,
    },
    {
      title: "Inbox",
      url: "#",
      icon: Inbox,
    },
    {
      title: "Calendar",
      url: "#",
      icon: Calendar,
    },
    {
      title: "References",
      url: "#",
      icon: BookMarked,
    },
  ]
  
  const subItems = [
    {
      title: "API",
      url: "/api",
      icon: ChevronsLeftRightEllipsis,
    },
    {
      title: "Help",
      url: "#",
      icon: CircleQuestionMark,
    },
    {
      title: "Settings",
      url: "settings",
      icon: Settings,
    },
  ]

  const [activeItem, setActiveItem] = useState<ItemType>(items[0])

  return(
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" asChild>
              <Link to="/">
                <div className="bg-sidebar-primary text-sidebar-primary-foreground flex aspect-square size-8 items-center justify-center rounded-lg">
                  <FlaskRound className="size-5" />
                </div>
                <div className="flex flex-col gap-0.5 leading-none">
                  <span className="font-large">FLASK</span>
                  <span className="">v0.0.0</span>
                </div>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          {/* <SidebarGroupLabel>Application</SidebarGroupLabel> */}
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton 
                    isActive={activeItem?.title === item.title}
                    onClick={() => setActiveItem(item)}
                    asChild
                  >
                    <Link to={item.url}>
                      <item.icon />
                      <span>{item.title}</span>
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        <SidebarGroup className="mt-auto">
          {/* <SidebarGroupLabel>Application</SidebarGroupLabel> */}
          <SidebarGroupContent>
            <SidebarMenu>
              {subItems.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton 
                    isActive={activeItem?.title === item.title}
                    onClick={() => setActiveItem(item)}
                    asChild
                  >
                    <Link to={item.url}>
                      <item.icon />
                      <span>{item.title}</span>
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
              <SidebarMenuItem>
                <Outlet />
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <NavUser />
      </SidebarFooter>
    </Sidebar>
  )
}
