import Landing from './landing';

export const metadata = {
  title: "AgentForge - Building agents for the future",
  description:
    "AgentForge is a tool to build and deploy advanced artifical intelligence multi-modal systems.",
  twitter: {
    card: "summary_large_image",
    title: "AgentForge - Building blocks for your Next.js project",
    description:
      "AgentForge is the all-in-one solution for your Next.js project. It includes a design system, authentication, analytics, and more.",
    creator: "@steventey",
  },
  metadataBase: new URL("https://github.com/fragro/agentforge"),
  themeColor: "#FFF",
};

export default async function Home() {
  const { stargazers_count: stars } = await fetch(
    "https://api.github.com/repos/steven-tey/precedent",
    {
      ...(process.env.GITHUB_OAUTH_TOKEN && {
        headers: {
          Authorization: `Bearer ${process.env.GITHUB_OAUTH_TOKEN}`,
          "Content-Type": "application/json",
        },
      }),
      // data will revalidate every 60 seconds
      next: { revalidate: 60 },
    },
  ).then((res) => res.json());

  return (
    <>
      <main className="flex min-h-screen w-full flex-col items-center justify-center py-32">
            <Landing />
      </main>
    </>
  );
}
