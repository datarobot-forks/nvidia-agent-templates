import { NavLink, Outlet } from 'react-router-dom';
import { ROUTES } from './routes';
import { cn } from '@/lib/utils';

const navItems = [
    { label: 'Connected sources', to: ROUTES.SETTINGS_SOURCES },
];

export const SettingsLayout = () => {
    return (
        <div className="flex flex-1 h-full justify-center">
            {/* Side navigation within settings */}
            <aside className="w-56 p-4 space-y-2">
                {navItems.map(item => (
                    <NavLink
                        key={item.to}
                        to={item.to}
                        className={({ isActive }) =>
                            cn(
                                'flex items-center gap-2 px-3 py-2 rounded-md text-sm hover:bg-accent',
                                isActive && 'bg-accent text-accent-foreground'
                            )
                        }
                    >
                        {item.label}
                    </NavLink>
                ))}
            </aside>

            {/* Active tab content */}
            <main className="w-full max-w-3xl overflow-y-auto px-6">
                <Outlet />
            </main>
        </div>
    );
};
