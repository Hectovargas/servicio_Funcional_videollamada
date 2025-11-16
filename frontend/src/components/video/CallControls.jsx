import { Button } from '@/components/ui/button';
import { Mic, MicOff, Video, VideoOff, Monitor, PhoneOff } from 'lucide-react';

export const CallControls = ({
  isMuted,
  isVideoOff,
  onToggleMute,
  onToggleVideo,
  onShareScreen,
  onLeave,
}) => {
  return (
    <div className="fixed bottom-6 left-1/2 transform -translate-x-1/2 z-50">
      <div className="flex gap-3 bg-gray-900/90 backdrop-blur-sm rounded-full px-4 py-3 shadow-xl">
        <Button
          variant={isMuted ? 'destructive' : 'secondary'}
          size="icon"
          onClick={onToggleMute}
          className="rounded-full"
        >
          {isMuted ? <MicOff className="h-5 w-5" /> : <Mic className="h-5 w-5" />}
        </Button>

        <Button
          variant={isVideoOff ? 'destructive' : 'secondary'}
          size="icon"
          onClick={onToggleVideo}
          className="rounded-full"
        >
          {isVideoOff ? <VideoOff className="h-5 w-5" /> : <Video className="h-5 w-5" />}
        </Button>

        <Button
          variant="secondary"
          size="icon"
          onClick={onShareScreen}
          className="rounded-full"
        >
          <Monitor className="h-5 w-5" />
        </Button>

        <Button
          variant="destructive"
          size="icon"
          onClick={onLeave}
          className="rounded-full"
        >
          <PhoneOff className="h-5 w-5" />
        </Button>
      </div>
    </div>
  );
};
