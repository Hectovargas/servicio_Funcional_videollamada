import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export const PreCallScreen = ({ onStartCall }) => {
  const [roomName, setRoomName] = useState('');
  const [userName, setUserName] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (roomName.trim() && userName.trim()) {
      onStartCall({
        room_name: roomName.trim(),
        user_name: userName.trim(),
        user_id: `user-${Date.now()}`,
        is_host: true,
      });
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 p-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Iniciar Videollamada</CardTitle>
          <CardDescription>
            Ingresa el nombre de la sala y tu nombre para comenzar
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="roomName">Nombre de la Sala</Label>
              <Input
                id="roomName"
                type="text"
                placeholder="Mi Sala"
                value={roomName}
                onChange={(e) => setRoomName(e.target.value)}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="userName">Tu Nombre</Label>
              <Input
                id="userName"
                type="text"
                placeholder="Tu Nombre"
                value={userName}
                onChange={(e) => setUserName(e.target.value)}
                required
              />
            </div>
            <Button type="submit" className="w-full">
              Iniciar Videollamada
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};
