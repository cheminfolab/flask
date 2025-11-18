import { 
  Calendar, 
  Home, 
  // Inbox, 
  Settings,
  FolderOpen,
  PillBottle,
  ChartColumn,
  Cpu,
  Bolt,
  FlaskRound,
  CircleQuestionMark,
  ChevronsLeftRightEllipsis,
  BookMarked
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
import { useState, type ComponentProps } from "react"
import { Link, Outlet } from "react-router"
 
export const AppSidebar = ({...props}: ComponentProps<typeof Sidebar>) => {

  // user, setUser = useContext()

  // Menu items.
  const items = [
    {
      title: "Home",
      url: "/",
      icon: Home,
    },
    {
      title: "Projects",
      url: "#",
      icon: FolderOpen,
    },
    {
      title: "Substances",
      url: "/substances",
      icon: Bolt,
    },
    {
      title: "Containers",
      url: "#",
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
    // {
    //   title: "Inbox",
    //   url: "#",
    //   icon: Inbox,
    // },
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

  const user = {
    name: "shadcn",
    email: "m@example.com",
    avatar: "/avatars/shadcn.jpg",
  }

  const [activeItem, setActiveItem] = useState(items[0])

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
                    isActive={activeItem.title === item.title}
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
                    isActive={activeItem.title === item.title}
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
                {/* <SettingsDialog /> */}
                <Outlet />
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={user} />
      </SidebarFooter>
    </Sidebar>
  )
}
