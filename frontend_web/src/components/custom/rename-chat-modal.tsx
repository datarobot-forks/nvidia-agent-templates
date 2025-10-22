import { Button } from '@/components/ui/button';
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useEffect, useMemo, useState } from 'react';
import { useAppState } from '@/state';
import { getChatNameOrDefaultWithTimestamp } from '@/lib/utils';
import { useChats, useChatsRename } from '@/api/chat/hooks.ts';

export const RenameChatModal = () => {
    const [name, setName] = useState<string>('');
    const [isComposing, setIsComposing] = useState(false);
    const { showRenameChatModalForId, setShowRenameChatModalForId } = useAppState();
    const { data: chats = [] } = useChats();
    const { mutate: renameChat, isPending } = useChatsRename();

    const chat = useMemo(() => {
        console.log('chats: %s', chats);
        return chats && chats.find(chat => chat.uuid === showRenameChatModalForId);
    }, [chats, showRenameChatModalForId]);

    useEffect(() => {
        if (chat) {
            setName(getChatNameOrDefaultWithTimestamp(chat));
        }
    }, [chat]);

    return (
        <Dialog defaultOpen={false} open={!!chat}>
            <DialogContent className="sm:max-w-[500px]">
                <DialogHeader>
                    <DialogTitle>Rename Chat</DialogTitle>
                </DialogHeader>
                <DialogDescription>
                    Enter a new name for your chat in the field below.
                </DialogDescription>
                <div className="grid gap-4 py-4">
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="name" className="text-right">
                            Name
                        </Label>
                        <Input
                            id="name"
                            value={name}
                            onChange={event => setName(event.target.value)}
                            className="col-span-3"
                            placeholder="Enter a name for your chat"
                            disabled={isPending}
                            onCompositionStart={() => setIsComposing(true)}
                            onCompositionEnd={() => setIsComposing(false)}
                            onKeyDown={event => {
                                if (event.key === 'Enter' && name.trim() && !isComposing) {
                                    renameChat(
                                        { chatId: chat!.uuid, chatName: name.trim() },
                                        {
                                            onSuccess: () => {
                                                setShowRenameChatModalForId(null);
                                            },
                                        }
                                    );
                                }
                            }}
                        />
                    </div>
                </div>
                <DialogFooter>
                    <Button
                        variant="ghost"
                        onClick={() => {
                            setName('');
                            setShowRenameChatModalForId(null);
                        }}
                    >
                        Cancel
                    </Button>
                    <Button
                        onClick={() => {
                            if (name.trim()) {
                                renameChat(
                                    { chatId: chat!.uuid, chatName: name.trim() },
                                    {
                                        onSuccess: () => {
                                            setShowRenameChatModalForId(null);
                                        },
                                    }
                                );
                            }
                        }}
                        disabled={isPending || !name.trim()}
                    >
                        {isPending ? 'Renaming...' : 'Rename'}
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
};
