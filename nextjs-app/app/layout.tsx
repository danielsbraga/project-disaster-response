// app/layout.tsx
import './globals.css';
import { Providers } from '@/components/providers';

export const metadata = {
  title: 'Disaster Response Classification',
  description: '…',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      {/* Não mexa no <html> aqui, o next-themes vai injetar a class no cliente */}
      <body>
        {/* Aqui é o ponto único para todos os provedores client-side */}
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}
