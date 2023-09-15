import "../styles/globals.css";
// import "../styles/style.scss";
import "../styles/style_demo.scss";
import { Analytics } from "@vercel/analytics/react";
import cx from "classnames";
import { sfPro, inter } from "../fonts";
import Nav_demo from "@/components/layout/nav_demo";
import Footer_demo from "@/components/layout/footer_demo";
import { Suspense } from "react";
import { ThemeProvider } from "@/components/ui/theme-provider";

export const metadata = {
  title: 'AgentForge',
  description: 'Build, design, and evaluate agents.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={cx(sfPro.variable, inter.variable)}>
        <div className="fixed h-screen w-full bg-white dark:bg-black" />
        <Suspense fallback="...">
          {/* @ts-expect-error Server Component */}
          {/*<Nav />*/}
          <div className="flex justify-center">
            <Nav_demo />
          </div>
        </Suspense>
        {/* <main className="flex min-h-screen w-full flex-col items-center justify-center py-32"> */}
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          {children}
        </ThemeProvider>
        {/* </main> */}
        <Analytics />
        {/* <Footer /> */}
        <Footer_demo />
      </body>
    </html>
  );
}
