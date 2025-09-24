export interface AppStateData {
    showRenameChatModalForId: string | null;
}

export interface AppStateActions {
    setShowRenameChatModalForId: (chatId: string | null) => void;
}

export type AppState = AppStateData & AppStateActions;

export type Action = {
    type: 'SET_SHOW_RENAME_CHAT_MODAL_FOR_ID';
    payload: { chatId: string | null };
};
