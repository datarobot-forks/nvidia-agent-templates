import { ChevronDown, MessagesSquare, UserRound } from 'lucide-react';
import { useNavigate, useLocation } from 'react-router-dom';
import drLogo from '@/assets/DataRobot_white.svg';
import drIcon from '@/assets/DataRobotLogo_black.svg';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { cn } from '@/lib/utils';
import {
    DropdownMenu,
    DropdownMenuTrigger,
    DropdownMenuContent,
    DropdownMenuItem,
} from '@/components/ui/dropdown-menu';
import {
    Sidebar,
    SidebarContent,
    SidebarFooter,
    SidebarMenu,
    SidebarMenuItem,
    SidebarMenuButton,
    SidebarHeader,
    SidebarGroup,
    useSidebar,
} from '@/components/ui/sidebar';
import { Button } from '@/components/ui/button.tsx';
import { Separator } from '@/components/ui/separator';

import { Link } from 'react-router-dom';
import { useCurrentUser } from '@/api/auth/hooks';
import { PATHS } from '@/constants/paths';
import { ChatList } from '@/components/custom/chat-list';

// Menu items.
const items = [
    {
        title: 'Chat',
        url: PATHS.CHAT,
        icon: MessagesSquare,
    },
];

export function AppSidebar() {
    const { open } = useSidebar();
    const { data: currentUser } = useCurrentUser();
    const navigate = useNavigate();
    const location = useLocation();

    const handleSettingsClick = () => {
        navigate(PATHS.SETTINGS.SOURCES);
    };
    return (
        <Sidebar collapsible="icon" className="bg-background" data-testid="app-sidebar">
            <SidebarHeader className="h-15 border-b">
                {open ? (
                    <Link to={PATHS.CHAT} className="ml-2.5 py-3.5 inline-block">
                        <img src={drLogo} alt="DataRobot" className="w-[130px]" />
                    </Link>
                ) : (
                    <Link to={PATHS.CHAT} className="ml-2 py-3 inline-block">
                        <img src={drIcon} alt="DataRobot" className="w-[20px]" />
                    </Link>
                )}
            </SidebarHeader>
            <SidebarContent className="pl-1">
                <SidebarMenu>
                    <SidebarGroup className="gap-2">
                        {items.map(item => (
                            <SidebarMenuItem
                                key={item.title}
                                className={cn(
                                    'flex gap-2 pr-3 pl-2 py-2 rounded-l-none border-l-2 border-transparent overflow-hidden transition-colors cursor-pointer hover:bg-card',
                                    {
                                        'rounded-l-none border-l-2 border-white bg-card':
                                            location.pathname === item.url,
                                    }
                                )}
                            >
                                <SidebarMenuButton
                                    asChild
                                    isActive={location.pathname === item.url}
                                >
                                    <Link to={item.url}>
                                        <item.icon />
                                        <span>{item.title}</span>
                                    </Link>
                                </SidebarMenuButton>
                            </SidebarMenuItem>
                        ))}
                        <Separator className="my-4 border-t" />
                        {open && (
                            <>
                                <p className="ml-1 text-base font-semibold">Chats</p>
                                <SidebarMenuItem>
                                    <SidebarMenuButton asChild>
                                        <ChatList />
                                    </SidebarMenuButton>
                                </SidebarMenuItem>
                            </>
                        )}
                    </SidebarGroup>
                </SidebarMenu>
            </SidebarContent>
            <SidebarFooter>
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <div className="h-9 flex w-full gap-1 ml-0.5 mb-2.5">
                            <Avatar>
                                <AvatarFallback>
                                    {currentUser &&
                                    currentUser.first_name &&
                                    currentUser.last_name ? (
                                        `${currentUser.first_name[0]}${currentUser.last_name[0]}`
                                    ) : (
                                        <UserRound />
                                    )}
                                </AvatarFallback>
                            </Avatar>
                            {open ? (
                                <Button
                                    variant="ghost"
                                    className="h-9 flex flex-1 w-full justify-between items-center gap-1 px-2 cursor-pointer hover:no-underline"
                                >
                                    <span>
                                        {(() => {
                                            const displayName =
                                                currentUser &&
                                                currentUser.first_name &&
                                                currentUser.last_name
                                                    ? `${currentUser.first_name} ${currentUser.last_name}`
                                                    : currentUser?.email || 'User';
                                            return displayName.length > 20
                                                ? `${displayName.slice(0, 20)}...`
                                                : displayName;
                                        })()}
                                    </span>
                                    <ChevronDown className="h-4 w-4" />
                                </Button>
                            ) : null}
                        </div>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                        <DropdownMenuItem>Profile</DropdownMenuItem>
                        <DropdownMenuItem
                            onSelect={handleSettingsClick}
                            data-testid="app-sidebar-settings-item"
                        >
                            Settings
                        </DropdownMenuItem>
                    </DropdownMenuContent>
                </DropdownMenu>
            </SidebarFooter>
        </Sidebar>
    );
}
