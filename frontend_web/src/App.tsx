/*
 * Copyright 2025 DataRobot, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
import { AppSidebar } from '@/components/layout/app-sidebar.tsx';
import { AppHeader } from '@/components/layout/app-header';
import Pages from '@/pages';
import { SidebarProvider } from '@/components/ui/sidebar';
import { Spinner } from '@/components/ui/spinner';


import './App.css';
import { useCurrentUser } from '@/api/auth/hooks.ts';
import { Toaster } from '@/components/ui/toast';
import { RenameChatModal } from '@/components/custom/rename-chat-modal.tsx';

function App() {
    const { isLoading: isUserLoading } = useCurrentUser();

    return (
        <SidebarProvider>
            <div className="flex flex-1 min-h-screen dark">
                <AppSidebar />
                <div className="flex flex-col flex-1 h-screen">
                    {isUserLoading ? (
                        <div
                            className="flex items-center gap-3 h-screen justify-center"
                            data-testid="app-loader"
                        >
                            <Spinner>Loading...</Spinner>
                        </div>
                    ) : (
                        <>
                            <AppHeader />
                            <Pages />
                            <Toaster />
                            <RenameChatModal />
                        </>
                    )}
                </div>
            </div>
        </SidebarProvider>
    );
}

export default App;
