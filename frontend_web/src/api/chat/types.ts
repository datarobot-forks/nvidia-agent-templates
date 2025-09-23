export interface IChatMessage {
    role: 'user' | 'assistant';
    content: string;
    chat_id?: string;
    components?: string;
    created_at?: string;
    error?: string;
    in_progress?: boolean;
    model?: string;
    uuid?: string;
}

export interface IUserMessage {
    message: string;
}

export interface IPostMessageContext {
    previousMessages: IChatMessage[];
    messagesKey: string[];
    previousChats?: IChat[];
}

export interface IChat {
    uuid: string;
    name: string;
    model: string;
    created_at: string; // ISO date for chat creation time
    updated_at: string; // ISO date for chat creation time
}

export interface IPostMessageParams {
    message: string;
    model?: string;
    chatId?: string;
    signal?: AbortSignal;
}
