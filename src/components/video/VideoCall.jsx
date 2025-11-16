import { useState } from 'react';
import { PreCallScreen } from './PreCallScreen';
import { CallControls } from './CallControls';
import { videoService } from '@/services/videoService';

export const VideoCall = () => {
  const [isInCall, setIsInCall] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [jitsiUrl, setJitsiUrl] = useState('');
  const [roomData, setRoomData] = useState(null);

  const handleStartCall = async (data) => {
    setIsLoading(true);
    setError(null);

    try {
      const authToken = 'test-token';
      const response = await videoService.createRoom(data, authToken);

      setRoomData(data);
      
      const urlWithJWT = response.jwt_token
        ? `${response.jitsi_url}?jwt=${response.jwt_token}&userInfo.displayName=${encodeURIComponent(data.user_name)}`
        : `${response.jitsi_url}?userInfo.displayName=${encodeURIComponent(data.user_name)}`;
      
      setJitsiUrl(urlWithJWT);
      setIsInCall(true);
      setIsLoading(false);
    } catch (err) {
      console.error('Error iniciando llamada:', err);
      setError(err.message || 'Error iniciando la videollamada');
      setIsLoading(false);
    }
  };

  const handleLeaveCall = () => {
    setIsInCall(false);
    setJitsiUrl('');
    setRoomData(null);
    setError(null);
  };

  const handleToggleMute = () => {
    console.log('Toggle mute - Los controles están en el iframe de Jitsi');
  };

  const handleToggleVideo = () => {
    console.log('Toggle video - Los controles están en el iframe de Jitsi');
  };

  const handleShareScreen = () => {
    console.log('Compartir pantalla - Usa el botón en el iframe de Jitsi');
  };

  if (!isInCall) {
    return <PreCallScreen onStartCall={handleStartCall} />;
  }

  return (
    <div className="relative w-full h-screen bg-gray-900">
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-gray-900/90 z-50">
          <div className="text-white text-lg">Cargando videollamada...</div>
        </div>
      )}

      {error && (
        <div className="absolute top-4 left-1/2 transform -translate-x-1/2 bg-red-600 text-white px-4 py-2 rounded-lg z-50">
          {error}
        </div>
      )}

      {jitsiUrl && (
        <iframe
          src={jitsiUrl}
          allow="camera; microphone; display-capture; fullscreen"
          style={{
            width: '100%',
            height: '100%',
            border: 'none',
          }}
          title="Jitsi Meet"
        />
      )}

      <CallControls
        isMuted={false}
        isVideoOff={false}
        onToggleMute={handleToggleMute}
        onToggleVideo={handleToggleVideo}
        onShareScreen={handleShareScreen}
        onLeave={handleLeaveCall}
      />
    </div>
  );
};
