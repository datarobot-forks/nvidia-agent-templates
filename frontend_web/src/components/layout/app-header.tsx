import { SidebarTrigger } from '@/components/ui/sidebar';
import { useIsMobile } from '@/hooks/use-mobile';

export function AppHeader() {


    const isMobile = useIsMobile();
    return (
        <header className="h-16 px-4 flex items-center justify-between" data-testid="app-header">
            <div className="flex gap-1">
                {isMobile && <SidebarTrigger className="h-9" />}
                
            </div>
        </header>
    );
}
