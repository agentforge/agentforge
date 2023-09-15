'use client';

import Balancer from "react-wrap-balancer";
import Image from "next/image";
import { useRouter } from 'next/navigation'
import Link from "next/link";
import { ModeToggle } from "@/components/ui/mode-toggle";
import { useTheme } from "next-themes";

// This is a Client Component. It receives data as props and
// has access to state and effects just like Page components
// in the `pages` directory.
export default function Landing_demo() {
  const router = useRouter();
  const { theme } = useTheme();

  return (
    <>
      <div className={"flex justify-self-center z-10 w-full max-w-[912px] pt-[144px] md:pt-[264px] px-[32px] md:px-0"}>
          <div className={"font-mono text-center text-black dark:text-white font-bold text-3xl md:text-7xl w-full"}>
            MULTI-MODAL AGENT
            INFRASTRUCTURE <br />
            FOR EVERYONE
          </div>
      </div>

      <div className={"flex justify-self-center z-10 w-full max-w-[912px] mt-[24px] md:mt-[64px] px-[32px] md:px-0"}>
          <div className={"font-mono text-center text-black dark:text-white text-sm md:text-lg w-full"}>
            Large language models provide a new probabilistic inference platform for building the next generation of agent applications
            <br/>AgentForge makes it easy
          </div>
      </div>


      <div id="sec-vision" className={"flex justify-self-center z-10 w-full max-w-[1120px] mt-[72px] md:mt-[176px] px-[32px] md:px-0"}>
          <div className={"font-mono text-center md:text-left text-black dark:text-zinc-400 text-sm md:text-lg w-full"}>
          WE ARE BUILDING INFRASTRUCTURE AT THE INTERSECTION BETWEEN
          </div>
      </div>

      <div className={"hidden md:flex justify-self-center z-10 w-full max-w-[1120px] mt-[8px] md:mt-[16px] px-[32px] md:px-0"}>
          <div className={"font-mono text-left text-black dark:text-white font-[300] md:text-4xl w-full"}>
          Human Cognition • Artificial Intelligence
          </div>
      </div>

      <div className={"flex md:hidden justify-self-center z-10 w-full max-w-[1120px] mt-[8px] md:mt-[16px] px-[32px] md:px-0"}>
          <div className={"font-mono text-center text-black dark:text-white font-[300] text-2xl w-full"}>
          Human Cognition<br />•<br />Artificial Intelligence
          </div>
      </div>

      {/* Meshes and images dervied from modified Human Face 3D model 
          Author: VistaPrime (https://sketchfab.com/VistaPrime)
          License: CC-BY-4.0 (http://creativecommons.org/licenses/by/4.0/)
          Source: https://sketchfab.com/3d-models/human-head-f46d952886ae4a8c8851341b810bba43
          Title: Human head */}

      {/* Section - 3-col Vision - Desktop */}
      <div className={"hidden md:flex justify-self-center z-10 w-full max-w-[1120px] mt-[64px] px-0"}>
        <div className="grid grid-cols-3 gap-[64px]">
          <div className="justify-self-start min-w-[208px] max-w-[330px]">
            {theme === 'light' ? (
              <Image alt="Stack of LLMs" src="/homepage/light_LLM_stack.svg" width={ 330 } height={ 406 }/>
            ) : (
              <Image alt="Stack of LLMs" src="/homepage/LLM_stack.svg" width={ 330 } height={ 406 }/>
              )
            }
            <div className="font-mono text-center text-black dark:text-white text-3xl mt-[32px]">LLM</div>
          </div>
          <div className="justify-self-center min-w-[208px] max-w-[330px]">
            <Image alt="Low poly face" src="/homepage/AvatarHead_face_front.png" width={ 330 } height={ 406 }/>
            <div className="font-mono text-center text-black dark:text-white text-3xl mt-[44px]">Multi-modal agent</div>
          </div>
          <div className="justify-self-end min-w-[208px] max-w-[330px]">
            {theme === 'light' ? (
              <Image alt="config JSON" src="/homepage/light_AgentForge_config.svg" width={ 330 } height={ 406 }/>
            ) : (
              <Image alt="config JSON" src="/homepage/AgentForge_config.svg" width={ 330 } height={ 406 }/>
              )
            }
            <div className="font-mono text-center text-black dark:text-white text-3xl mt-[44px]">AgentForge</div>
          </div>
        </div>
      </div>
      {/* End of Section - 3-col Vision - Desktop */}

      {/* Section - 3-col Vision - Mobile - scrolling */}
      <div className={"flex md:hidden overflow-x-scroll"}>
        <div className={"flex md:hidden justify-self-left z-10 w-full min-w-[717px] mt-[48px] px-[32px]"}>
          <div className="grid grid-cols-3 gap-[24px]">
            <div className="justify-self-start min-w-[208px] max-w-[330px]">
              <Image alt="Stack of LLMs" src="/homepage/LLM_stack.svg" width={ 330 } height={ 406 }/>
              <div className="font-mono text-center text-black dark:text-white text-xl mt-[24px]">LLM</div>
            </div>
            <div className="justify-self-center min-w-[208px] max-w-[330px]">
              <Image alt="Low poly face" src="/homepage/AvatarHead_face_front.png" width={ 330 } height={ 406 }/>
              <div className="font-mono text-center text-black dark:text-white text-xl mt-[32px]">Multi-modal agent</div>
            </div>
            <div className="justify-self-end min-w-[208px] max-w-[330px]">
              <Image alt="config JSON" src="/homepage/AgentForge_config.svg" width={ 330 } height={ 406 }/>
              <div className="font-mono text-center text-black dark:text-white text-xl mt-[32px]">AgentForge</div>
            </div>
          </div>
        </div>
      </div>
      {/* End of Section - 3-col Vision - Mobile - scrolling */}
      
      
      <div id="sec-cognition" className={"flex justify-self-center z-10 w-full max-w-[1120px] mt-[72px] md:mt-[176px] px-[32px] md:px-0"}>
          <div className={"font-mono text-center md:text-left text-black dark:text-zinc-400 text-sm md:text-lg w-full"}>
          AUTONOMOUS ONLINE AGENTS AS A PLATFORM FOR
          </div>
      </div>

      <div className={"flex justify-self-center z-10 w-full max-w-[1120px] mt-[8px] md:mt-[16px] px-[32px] md:px-0"}>
          <div className={"font-mono text-center md:text-left text-black dark:text-white font-[300] text-2xl md:text-4xl w-full"}>
          Cognition Engine
          </div>
      </div>

      {/* Section - 5-col Cognition engine - Desktop */}
      <div className={"hidden md:flex justify-self-center z-10 w-full max-w-[1120px] mt-[64px] px-0"}>
        <div className="grid grid-cols-5 gap-[20px]">
          <div className="justify-self-start max-w-[208px]">
            <Image alt="Human facing right" src="/homepage/Humanhead_face_right.png" width={ 208 } height={ 406 }/>
            <div className="font-mono text-center text-black dark:text-white text-3xl mt-[32px]">Human</div>
          </div>
          <div className="justify-self-center max-w-[208px]">
            {theme === 'light' ? (
              <Image alt="Conversation text bubbles" src="/homepage/light_Conversation.svg" width={ 208 } height={ 406 }/>
            ) : (
              <Image alt="Conversation text bubbles" src="/homepage/Conversation.svg" width={ 208 } height={ 406 }/>
            )}
            <div className="font-mono text-center text-black dark:text-white text-3xl mt-[32px]"> </div>
          </div>
          <div className="justify-self-center max-w-[208px]">
            <Image alt="Avatar facing left" src="/homepage/Avatarhead_face_left.png" width={ 208 } height={ 406 }/>
            <div className="font-mono text-center text-black dark:text-white text-3xl mt-[32px]">Agent</div>
          </div>
          <div className="col-span-2 justify-self-end max-w-[436px]">
            {theme === 'light' ? (
              <Image alt="Conversation text bubbles" src="/homepage/light_Cognition.svg" width={ 436 } height={ 406 }/>
            ) : (
              <Image alt="Conversation text bubbles" src="/homepage/Cognition.svg" width={ 436 } height={ 406 }/>
            )}
            <div className="font-mono text-center text-black dark:text-white text-3xl mt-[32px]">Cognition</div>
          </div>
        </div>
      </div>
      {/* End of Section - 5-col Cognition engine - Desktop */}

      {/* Section - 1-col Cognition engine - Mobile */}
      <div className="flex md:hidden grid grid-cols-1 justify-self-center z-10 w-full max-w-[1120px] mt-[8px] md:mt-[16px] px-[32px] md:px-0">
          <Image alt="Abstract cognition" src="/homepage/Cognition.svg" className="justify-self-center" width={ 436 } height={ 406 }/>
          {/*<div className="font-mono text-center text-white text-xl mt-[24px]"> </div>*/}
      </div>
      {/* End of Section - 1-col Cognition engine - Mobile */}

      
      <div id="sec-projects" className={"flex justify-self-center z-10 w-full max-w-[1120px] mt-[72px] md:mt-[176px] px-[32px] md:px-0"}>
          <div className={"font-mono text-center md:text-left text-black dark:text-zinc-400 text-sm md:text-lg w-full"}>
          A SNEAK PEEK OF OUR
          </div>
      </div>

      <div className={"flex justify-self-center z-10 w-full max-w-[1120px] mt-[8px] md:mt-[16px] px-[32px] md:px-0"}>
          <div className={"font-mono text-center md:text-left text-black dark:text-white font-[300] text-2xl md:text-4xl w-full"}>
          Projects
          </div>
      </div>

      {/* Section - 3-col Projects - Desktop */}
      <div className={"hidden lg:flex justify-self-center z-10 w-full max-w-[1120px] mt-[64px] px-0"}>
        <div className={"grid grid-cols-3 gap-[40px]"}>
          <div className={"col-span-2 grid grid-cols-2 gap-[20px] justify-self-start" +  
                          "min-w-[750px] rounded-[8px] border-2 border-black dark:border-zinc-600 " + 
                          "shadow-[0_12px_50px_-9px_rgba(255, 255, 255, 0.48)] " + 
                          "p-[64px] pb-[48px]"}
            >
            <div>
              <div className={"font-mono text-left text-black dark:text-white text-5xl w-full"}>
                Almanac
              </div>
              <div className={"font-mono text-left text-black dark:text-white text-lg w-full pt-[36px]"}>
                An on-demand virtual assistant which guides end-users with planning activities requiring specialized knowledge
              </div>
              <div className={"font-mono text-left text-black dark:text-white text-lg w-full pt-[36px]"}>
                For Small Businesses and startups to provide technical support at scale
              </div>
            </div>
            <div>
              <video autoPlay muted loop className={"w-full rounded-[16px] border-2 border-black dark:border-zinc-600"}>         
                  <source src="/homepage/almanac_idle_loop.mp4" type="video/mp4"/>       
              </video>
              <button
                className={"w-full mt-[24px] font-mono rounded-[4px] p-[10px] px-4 " + 
                            "text-base font-medium text-white bg-black dark:text-black dark:bg-white transition-all hover:bg-white/60"}
                onClick={() => router.push('/demo')}
              >
                Chat with Gardener-Almanac
              </button>
            </div>
          </div>

          <div className={"justify-self-end min-w-[330px] grid grid-cols-1 gap-[32px]"}>
            <div className={"rounded-[8px] border-2 border-black dark:border-zinc-600 p-[32px]"}>
              <div className={"font-mono text-left text-black dark:text-white text-5xl w-full"}>
                Caretaker
              </div>
              <div className={"font-mono text-left text-black dark:text-white text-lg w-full pt-[36px]"}>
                An always on agent with capabilities, TBA
              </div>
            </div>
            <div className={"rounded-[8px] border-2 border-black dark:border-zinc-600 p-[32px]"}>
              <div className={"font-mono text-left text-black dark:text-white text-5xl w-full"}>
                The Forge
              </div>
              <div className={"font-mono text-left text-black dark:text-white text-lg w-full pt-[36px]"}>
                No-code GUI for agent-avatar creation, training and deployment, TBA
              </div>
            </div>
          </div>
        </div>
      </div>
      {/* End of Section - 3-col Projects - Desktop */}

      {/* Section - 1-col Projects - Mobile */}
      <div className="flex lg:hidden grid grid-cols-1 justify-self-center z-10 w-full max-w-[1120px] mt-[44px] px-[32px]">
        <div className={"rounded-[8px] border-2 border-black dark:border-zinc-600 " +
                        "shadow-[0_12px_50px_-9px_rgba(255, 255, 255, 0.48)] " + 
                        "p-[32px]"}
              >
            <div>
              <div className={"font-mono text-center text-black dark:text-white text-3xl w-full"}>
                Almanac
              </div>

              <div>
              <video autoPlay muted loop className={"w-full rounded-[16px] border-2 border-black dark:border-zinc-600 mt-[24px]"}>         
                  <source src="/homepage/almanac_idle_loop.mp4" type="video/mp4"/>       
              </video>
              <button
                className={"w-full mt-[24px] font-mono rounded-[4px] py-[10px] px-[16px] " + 
                            "text-base font-medium text-white bg-black dark:text-black dark:bg-white transition-all hover:bg-white/60"}
                onClick={() => router.push('/demo')}
              >
                Chat with <br/> Gardener-Almanac
              </button>
            </div>

              <div className={"font-mono text-center text-black dark:text-white text-base w-full pt-[36px]"}>
                An on-demand virtual assistant which guides end-users with planning activities requiring specialized knowledge
              </div>
              <div className={"font-mono text-center text-black dark:text-white text-base w-full pt-[36px]"}>
                For Small Businesses and startups to provide technical support at scale
              </div>
            </div>
            
          </div>

          <div className={"rounded-[8px] border-2 border-black dark:border-zinc-600 " +
                        "p-[32px] mt-[24px]"}
              >
            <div>
              <div className={"font-mono text-center text-black dark:text-white text-3xl w-full"}>
                Caretaker
              </div>

              <div className={"font-mono text-center text-black dark:text-white text-base w-full pt-[36px]"}>
                An always on agent with capabilities, TBA
              </div>

            </div>
            
          </div>

          <div className={"rounded-[8px] border-2 border-black dark:border-zinc-600 " +
                        "p-[32px] mt-[24px]"}
              >
            <div>
              <div className={"font-mono text-center light:text-black dark:text-white text-3xl w-full"}>
                The Forge
              </div>

              <div className={"font-mono text-center text-black dark:text-white text-base w-full pt-[36px]"}>
                No-code GUI for agent-avatar creation, training and deployment, TBA
              </div>

            </div>
            
          </div>
      </div>
      {/* End of Section - 1-col Projects - Mobile */}
      
      <div className="fixed bottom-0 right-0 mb-4 mr-4 z-50">
        <ModeToggle />
      </div>

      <div className={"flex justify-self-center z-10 w-full max-w-[1120px] mt-[72px] md:mt-[120px] px-[32px] md:px-0"}>
          <div className={"font-mono text-center text-black dark:text-white font-[300] text-2xl md:text-4xl w-full"}>
            Contact Us
          </div>
      </div>

      <div className={"flex justify-self-center z-10 w-full max-w-[1120px] mt-[24px] md:mt-[20px] px-[32px] md:px-0"}>
          <div className={"font-mono text-center text-black dark:text-white font-[300] text-xl md:text-2xl w-full underline decoration-2"}>
            <Link href="mailto:info@agentforge.ai" >
              info@agentforge.ai
            </Link>
          </div>
      </div>
      
      <div className={"flex justify-self-center z-10 w-auto mt-[24px] md:mt-[16px] px-[32px] md:px-0"}>
        <div>
        {theme === 'light' ? (
              <Link href="https://github.com/agentforge/" className="flex items-center">
              <Image
                src="/homepage/light_Github.svg"
                alt="Github logo"
                width="36"
                height="36"
                className="rounded-sm transition-all hover:fill-white/50"
                
              ></Image>
            </Link>
            ) : (
              <Link href="https://github.com/agentforge/" className="flex items-center">
                <Image
                  src="/homepage/Github.svg"
                  alt="Github logo"
                  width="36"
                  height="36"
                  className="rounded-sm transition-all hover:fill-white/50"
                  style={{color: "#fff", fill: "#fff"}}
                ></Image>
              </Link>
              )
            }
        </div>
        <div className="pl-[16px]">
          {theme === 'light' ? (
              <Link href="https://twitter.com/agentforge_ai/" className="flex items-center">
              <Image
                src="/homepage/light_Twitter.svg"
                alt="Github logo"
                width="36"
                height="36"
                className="rounded-sm transition-all hover:fill-white/50"
               
              ></Image>
            </Link>
            ) : (
              <Link href="https://twitter.com/agentforge_ai/" className="flex items-center">
                <Image
                  src="/homepage/Twitter.svg"
                  alt="Github logo"
                  width="36"
                  height="36"
                  className="rounded-sm transition-all hover:fill-white/50"
                  style={{color: "#fff", fill: "#fff"}}
                ></Image>
              </Link>
              )
            }
        </div>
      </div>
    </>
  );
}


