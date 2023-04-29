import Card from "@/components/home/card";
import DualCard from "@/components/home/dualcard";
import Balancer from "react-wrap-balancer";
import { DEPLOY_URL } from "@/lib/constants";
import { Github, Twitter } from "@/components/shared/icons";
import WebVitals from "@/components/home/web-vitals";
import ComponentGrid from "@/components/home/component-grid";
import Image from "next/image";
import { nFormatter } from "@/lib/utils";

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
      <div className="z-10 w-full max-w-xl px-5 xl:px-0">
        {/* <a
          href="https://twitter.com/steventey/status/1613928948915920896"
          target="_blank"
          rel="noreferrer"
          className="mx-auto mb-5 flex max-w-fit animate-fade-up items-center justify-center space-x-2 overflow-hidden rounded-full bg-blue-100 px-7 py-2 transition-colors hover:bg-blue-200"
        >
          <Twitter className="h-5 w-5 text-[#1d9bf0]" />
          <p className="text-sm font-semibold text-[#1d9bf0]">
            PersonaForge
          </p>
        </a> */}
        <h1
          className="animate-fade-up bg-gradient-to-br from-black to-stone-500 bg-clip-text text-center font-display text-4xl font-bold tracking-[-0.02em] text-transparent opacity-0 drop-shadow-sm md:text-7xl md:leading-[5rem]"
          style={{ animationDelay: "0.15s", animationFillMode: "forwards" }}
        >
          <Balancer>Building accessible agents for the people</Balancer>
        </h1>
        <p
          className="mt-6 animate-fade-up text-center text-gray-500 opacity-0 md:text-xl"
          style={{ animationDelay: "0.25s", animationFillMode: "forwards" }}
        >
          <Balancer>
            Build, deploy, and manage your agents with ease.
          </Balancer>
        </p>
        <div
          className="mx-auto mt-6 flex animate-fade-up items-center justify-center space-x-5 opacity-0"
          style={{ animationDelay: "0.3s", animationFillMode: "forwards" }}
        >
          <a
            className="group flex max-w-fit items-center justify-center space-x-2 rounded-full border border-black bg-black px-5 py-2 text-sm text-white transition-colors hover:bg-white hover:text-black"
            href="/register"
            target="_blank"
            rel="noopener noreferrer"
          >
            <p>Register</p>
          </a>
          {/* <a
            className="flex max-w-fit items-center justify-center space-x-2 rounded-full border border-gray-300 bg-white px-5 py-2 text-sm text-gray-600 shadow-md transition-colors hover:border-gray-800"
            href="https://github.com/steven-tey/precedent"
            target="_blank"
            rel="noopener noreferrer"
          >
            <Github />
            <p>
              <span className="hidden sm:inline-block">Star on</span> GitHub{" "}
              <span className="font-semibold">{nFormatter(stars)}</span>
            </p>
          </a> */}
        </div>
      </div>
      <div className="my-10 grid w-full max-w-screen-xl animate-fade-up grid-cols-1 gap-5 px-5 md:grid-cols-3 xl:px-0">
        {features.map(({ title, description, demo, large }) => (
          title === "Building Next Generation Agent Applications" ? (
            <DualCard
              key={title}
              title={title}
              description={description}
              demo={(demo)}
              large={large}
            />
          ) : (
            <Card
              key={title}
              title={title}
              description={description}
              demo={(demo)}
              large={large}
            />
          )
          
        ))}
      </div>
    </>
  );
}

const features = [
  {
    title: "Multi-Modal",
    description:
      "Large Language Models, Speech Synthesis, Speech Recognition, Computer Vision, and more",
    demo: (
      <a href={DEPLOY_URL}>
        <div className="grid grid-flow-col grid-rows-3 gap-10 p-10">
        <span className="font-mono font-semibold">Alpaca 7B</span>
        <span className="font-mono font-semibold">Whisper JAX</span>
        <span className="font-mono font-semibold">coqai TTS</span>
        <span className="font-mono font-semibold">PRISMER</span>
        <span className="font-mono font-semibold">Wav2Lip</span>
        <span className="font-mono font-semibold">DeepLake</span>
      </div>
      </a>
    ),
  },
  {
    title: "Configurable",
    description:
      "Configure your agent, models, and voice synthesizer with a simple JSON file",
    demo: (
      <div className="flex items-center justify-center space-x-20">
        <Image alt="JSON vector logo" src="/json.svg" width={ 100 } height={ 100 }/>
      </div>
    ),
  },
  {
    title: "Agent Based",
    description:
      "PersonaForge gives you the tools to build complex online agents with control flow over model interfaces",
    demo: (
      <div className="grid grid-flow-col grid-rows-3 gap-5 p-10">
        <span className="font-mono font-semibold">Prompt Management</span>
        <span className="font-mono font-semibold">VectorStore Memory</span>
        <span className="font-mono font-semibold">Reflection</span>
        <span className="font-mono font-semibold">Guardrails</span>
        <span className="font-mono font-semibold">Avatar Management</span>
        <span className="font-mono font-semibold">Online Agent</span>
      </div>
    ),
  },
  {
    title: "Building Next Generation Agent Applications",
    description:
      "Language models provide a new probabilistic interface for building agent applications and with it comes new challenges. PersonaForge makes it easy",
    large: true,
    demo: (
        <Image alt="JSON vector logo" src="/agent1.png" width={ 350 } height={ 150 }/>
    ),
  },
  {
    title: "Local First Models",
    description:
      "PersonaForge is built to be deployed anywhere without need for external APIs or services",
    demo: (
      <Image alt="Open Source Logo" src="/agent2.png" width={200} height={200} />
    ),
  },
];
