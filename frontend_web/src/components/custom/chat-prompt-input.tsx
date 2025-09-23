import { useCallback, useState, useMemo } from 'react';
import { useParams } from 'react-router-dom';

import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import {
    Send,
} from 'lucide-react';
import { useCreateChat, usePostMessage } from '@/api/chat/hooks.ts';
import { cn } from '@/lib/utils.ts';

export function ChatPromptInput({
    classNames,
    hasPendingMessage,
}: {
    classNames?: string;
    hasPendingMessage: boolean;
}) {
    const { chatId } = useParams<{ chatId: string }>();
    const [message, setMessage] = useState<string>('');
    const { mutateAsync: sendMessage, isPending: isSendingMessage } = usePostMessage({ chatId });
    const { mutateAsync: startChat, isPending: isStartingChat } = useCreateChat();

    const [isComposing, setIsComposing] = useState(false);

    const isPromptPending = useMemo(
        () => hasPendingMessage || isSendingMessage || isStartingChat,
        [hasPendingMessage, isSendingMessage, isStartingChat]
    );


    const handleSubmit = useCallback(async () => {
        if (message) {
            try {
                if (chatId) {
                    await sendMessage({
                        message,
                    });
                } else {
                    await startChat({
                        message,
                    });
                }
            } finally {
                setMessage('');
            }
        }
    }, [sendMessage, startChat, chatId, message, setMessage]);

    const handleEnterPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey && !isComposing) {
            e.preventDefault();
            handleSubmit();
        }
    };

    return (
        <>
            <div
                className={cn(
                    isPromptPending ? 'cursor-wait opacity-70' : '',
                    'transition-all',
                    'justify-items-center p-5 w-2xl',
                    classNames
                )}
                data-testid="chat-prompt-input"
            >
                <Textarea
                    disabled={isPromptPending}
                    onChange={e => setMessage(e.target.value)}
                    placeholder="Ask anything..."
                    value={message}
                    className={cn(
                        isPromptPending && 'pointer-events-none',
                        'resize-none rounded-none',
                        'dark:bg-muted border-gray-700'
                    )}
                    onKeyDown={handleEnterPress}
                    onCompositionStart={() => setIsComposing(true)}
                    onCompositionEnd={() => setIsComposing(false)}
                    data-testid="chat-prompt-input-textarea"
                />
                <div className="w-full p-1 border border-t-0 border-gray-700">
                    <div className="flex items-center justify-between h-12">
                        <Button
                            className="justify-self-end cursor-pointer"
                            variant="ghost"
                            size="icon"
                            onClick={handleSubmit}
                            data-testid="chat-prompt-input-submit"
                            disabled={isPromptPending}
                        >
                            <Send />
                        </Button>
                    </div>
                </div>
            </div>
        </>
    );
}
