import { useMutation, useQueryClient, useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';
import {
    deleteChatById,
    renameChatById,
    getAllChats,
    getMessages,
    postMessage,
    startNewChat,
} from './requests';
import { chatKeys } from './keys';
import { IChatMessage, IPostMessageContext, IUserMessage, IChat } from './types';

export const useCreateChat = () => {

    const queryClient = useQueryClient();
    const navigate = useNavigate();

    return useMutation<IChat, Error, IUserMessage, IPostMessageContext>({
        mutationFn: ({ message }) => {
            return startNewChat({
                message: message
            });
        },
        onError: error => {
            toast.error(error?.message || 'Failed to send message');
        },
        onSuccess: data => {
            queryClient.setQueryData<IChat[]>(chatKeys.all, (oldData = []) => [...oldData, data]);
            queryClient.invalidateQueries({ queryKey: chatKeys.chatList() });
            navigate(`/chat/${data.uuid}`);
        },
    });
};

export const usePostMessage = ({ chatId }: { chatId?: string }) => {
    const queryClient = useQueryClient();
    return useMutation<IChatMessage[], Error, IUserMessage, IPostMessageContext>({
        mutationFn: ({ message }) => {
            if (!chatId) {
                throw new Error('chatId is required');
            }

            return postMessage({
                message: message,
                chatId,
            });
        },
        onError: (error, _variables, context) => {
            // Restore previous messages
            if (context?.previousMessages && context?.messagesKey) {
                queryClient.setQueryData(context.messagesKey, context.previousMessages);
            }
            toast.error(error?.message || 'Failed to send message');
        },
        onSuccess: data => {
            // Set the chat messages data directly in the cache to avoid loading state
            queryClient.setQueryData<IChatMessage[]>(chatKeys.messages(chatId), (oldData = []) => [
                ...oldData,
                ...data,
            ]);
            queryClient.setQueryData<IChat[]>(chatKeys.chatList(), (oldData = []) => {
                return oldData.map(chat =>
                    chat.uuid === chatId
                        ? ({ ...chat, updated_at: data[data.length - 1].created_at } as IChat)
                        : chat
                );
            });
        },
    });
};

export const useChatMessages = ({
    chatId,
    shouldRefetch,
}: {
    chatId?: string;
    shouldRefetch?: number;
}) => {
    return useQuery<IChatMessage[]>({
        queryKey: chatKeys.messages(chatId),
        queryFn: async ({ signal }) => {
            return await getMessages({ chatId: chatId!, signal });
        },
        enabled: !!chatId,
        refetchInterval: shouldRefetch || false,
    });
};

export const useChats = () => {
    return useQuery<IChat[]>({
        queryKey: chatKeys.chatList(),
        queryFn: async ({ signal }) => {
            return await getAllChats(signal);
        },
        staleTime: 60000, // Use 1 minute, we have invalidate calls when item is changed/deleted
    });
};

export const useChatsDelete = () => {
    const queryClient = useQueryClient();
    return useMutation<void, Error, { chatId: string }>({
        mutationFn: ({ chatId }) => deleteChatById({ chatId }),
        onSuccess: () => queryClient.invalidateQueries({ queryKey: chatKeys.chatList() }),
    });
};

export const useChatsRename = () => {
    const queryClient = useQueryClient();
    return useMutation<void, Error, { chatId: string; chatName: string }>({
        mutationFn: ({ chatId, chatName }) => renameChatById({ chatId, chatName }),
        onSuccess: () => queryClient.invalidateQueries({ queryKey: chatKeys.chatList() }),
    });
};
