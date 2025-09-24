import { lazy } from 'react';
import { Navigate } from 'react-router-dom';

import { SettingsLayout } from './pages/SettingsLayout';
import { SettingsSources } from './pages/SettingsSources';
import { PATHS } from '@/constants/paths';

// Lazy-loaded pages
const ChatPage = lazy(() => import('./pages/Chat'));
const OAuthCallback = lazy(() => import('./pages/OAuthCallback'));

export const appRoutes = [
    { path: PATHS.CHAT, element: <ChatPage /> },
    { path: PATHS.CHAT_PAGE, element: <ChatPage /> },
    {
        path: PATHS.SETTINGS.ROOT,
        element: <SettingsLayout />,
        children: [
            { index: true, element: <Navigate to="sources" replace /> },
            { path: 'sources', element: <SettingsSources /> },
        ],
    },
    { path: PATHS.OAUTH_CB, element: <OAuthCallback /> },
    { path: '*', element: <Navigate to={PATHS.CHAT} replace /> },
];
