import React, { useReducer } from 'react';
import { AppState, AppStateData } from './types';
import { reducer, createInitialState, actions } from './reducer';
import { AppStateContext } from './AppStateContext';

export const AppStateProvider: React.FC<{
    children: React.ReactNode;
    initialState?: AppStateData;
}> = ({ children, initialState }) => {
    const [state, dispatch] = useReducer(reducer, initialState ?? createInitialState());

    const setShowRenameChatModalForId = (chatId: string | null) => {
        dispatch(actions.setShowRenameChatModalForId(chatId));
    };

    const contextValue: AppState = {
        ...state,
        setShowRenameChatModalForId,
    };

    return <AppStateContext.Provider value={contextValue}>{children}</AppStateContext.Provider>;
};
