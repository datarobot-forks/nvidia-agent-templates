import { AppStateData, Action } from './types';
import { ACTION_TYPES, DEFAULT_VALUES } from './constants';

export const createInitialState = (): AppStateData => {
    return {
        showRenameChatModalForId: DEFAULT_VALUES.showRenameChatModalForId,
    };
};

export const reducer = (state: AppStateData, action: Action): AppStateData => {
    switch (action.type) {
        case ACTION_TYPES.SET_SHOW_RENAME_CHAT_MODAL_FOR_ID:
            return {
                ...state,
                showRenameChatModalForId: action.payload.chatId,
            };
        default:
            return state;
    }
};

export const actions = {
    setShowRenameChatModalForId: (chatId: string | null): Action => ({
        type: ACTION_TYPES.SET_SHOW_RENAME_CHAT_MODAL_FOR_ID,
        payload: { chatId },
    }),
};
