"use client";

import Image from "next/image";
import Link from "next/link";
import useScroll from "@/lib/hooks/use-scroll";
import UserDropdown from "./user-dropdown";
import { Session } from "next-auth";
import { useRouter } from 'next/navigation'
import { Fragment, useState } from 'react'


export default function Navbar_demo() {

  const scrolled = useScroll(50);
  const router = useRouter();

  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)


  return (
    <>
    {/* Header - outer container */}
      <div
        className={"fixed pt-[16px] md:pt-[64px] pb-[16px] md:pb-[24px] w-screen backdrop-blur-xl z-30"}
      >
        {/* Header - desktop */}
        <div className="hidden md:flex w-[1120px] mx-5 flex h-16 max-w-screen-xl items-center justify-between xl:mx-auto ">
          {/*Logotype - left algined*/}
          <Link href="/" className="flex items-center font-display text-2xl text-black dark:text-white">
            <Image
              src="/agentforge-logo.svg"
              alt="AgentForge logo"
              width="28"
              height="28"
              className="mr-2 rounded-sm"
              style={{color: "#fff", fill: "#fff"}}
            ></Image>
            <p>AgentForge</p>
          </Link>

          {/* Nav menu - full sized */}
          {/* Ref: https://tailwindui.com/components/marketing/elements/headers */}
          <div className="hidden md:flex md:gap-x-[96px] md:pt-[8px]">
            <div className="relative">
              <button type="button" className="flex items-center gap-x-1 font-mono text-lg font-medium leading-6 text-black dark:text-white"
                      onClick={() => router.push('#sec-vision')}
              >
                Vision
              </button>
            </div>
          </div>

          <div className="hidden md:flex md:gap-x-[48px] md:pt-[8px]">
            <div className="relative">
              <button type="button" className="flex items-center gap-x-1 font-mono text-lg font-medium leading-6 text-black dark:text-white"
                      onClick={() => router.push('#sec-cognition')}
              >
                Cognition engine
              </button>
            </div>
          </div>

          <div className="hidden md:flex md:gap-x-[48px] md:pt-[8px]">
            <div className="relative">
              <button type="button" className="flex items-center gap-x-1 font-mono text-lg font-medium leading-6 text-black dark:text-white" 
                      onClick={() => router.push('#sec-projects')}
              >
                Projects
              </button>
            </div>
          </div>

          {/*DEMO button - right algined*/}
          <div className="md:visible">
              <button
                className="font-mono rounded-[4px] border-2 border-black dark:border-white p-1.5 px-4 text-base text-black dark:text-white transition-all hover:bg-white/50"
                onClick={() => router.push('/demo')}
              >
                DEMO
              </button>
          </div>
        </div> {/* End of: Header - desktop */}




        {/* Header - mobile */}
        <div className="mx-5 flex h-16 max-w-screen-xl items-center justify-between xl:mx-auto md:hidden">
          {/*DEMO button - left algined*/}
            <div className="md:hidden">
              <button
                className="font-mono rounded-[4px] border-2 border-black dark:border-white p-1.5 px-4 text-sm text-black dark:text-white transition-all hover:bg-white/50"
                onClick={() => router.push('/demo')}>
                DEMO
              </button>
            </div>


          {/*Logotype - center algined*/}
          <Link href="/" className="flex items-center font-display text-2xl -ml-[36px]">
            <Image
              src="/agentforge-logo.svg"
              alt="AgentForge logo"
              width="28"
              height="28"
              className="rounded-sm"
              style={{color: "#fff", fill: "#fff"}}
            ></Image>
          </Link>

          
          <div className="md:invisble">
            {/* Hamburger button and menu - right algined*/}
            {mobileMenuOpen ? (
              <div className="md:hidden" role="dialog" aria-modal="true">
                <div className="fixed inset-0 z-50"></div>
                  <div className="fixed inset-y-0 right-0 z-50 w-full overflow-y-auto h-[240px] bg-white/60 backdrop-blur-sm px-6 py-6 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10 rounded-b-lg">
                    <div className="flex items-center justify-between  pt-[12px]">
                      <a href="#" className="-m-1.5 p-1.5">
                        <span className="sr-only"> </span>
                      </a>
                      <button type="button" className="-m-2.5 rounded-md p-2.5 text-gray-700"
                        onClick={() => setMobileMenuOpen(false)} >
                        <span className="sr-only">Close menu</span>
                        <svg className="h-6 w-6" fill="black" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </div>
                    <div className="mt-6 flow-root">
                      <div className="-my-6 divide-y divide-gray-500/10">
                        <div className="space-y-2 py-6">
                          <div className="-mx-3">
                            <button type="button" className={"flex w-full items-center justify-between rounded-lg " + 
                                                              "py-2 pl-3 pr-3.5 font-mono text-base font-semibold " + 
                                                              "leading-7 text-black dark:text-white hover:bg-gray-50"} 
                                    aria-controls="disclosure-1" aria-expanded="false"
                                    onClick={() => {router.push('#sec-vision'); setMobileMenuOpen(false);}}
                            >
                              Vision
                            </button>
                            <button type="button" className={"flex w-full items-center justify-between rounded-lg " + 
                                                              "py-2 pl-3 pr-3.5 text-base font-mono font-semibold " + 
                                                              "leading-7 text-black dark:text-white hover:bg-gray-50"} 
                                    aria-controls="disclosure-1" aria-expanded="false"
                                    onClick={() => {router.push('#sec-cognition'); setMobileMenuOpen(false);}}
                            >
                              Cognition engine
                            </button>
                            <button type="button" className={"flex w-full items-center justify-between rounded-lg " + 
                                                              "py-2 pl-3 pr-3.5 text-base font-mono font-semibold " + 
                                                              "leading-7 text-black dark:text-white hover:bg-gray-50"} 
                                    aria-controls="disclosure-1" aria-expanded="false"
                                    onClick={() => {router.push('#sec-projects'); setMobileMenuOpen(false);}}
                            >
                              Projects
                            </button>
                          
                          </div>
                        </div>
                      </div>
                    </div>
                </div>
              </div>
              ) : ( 
                <div className="flex lg:hidden">
                <button type="button" className="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-black dark:text-white"
                onClick={() => setMobileMenuOpen(true)} >
                  <span className="sr-only">Open main menu</span>
                  <svg className="h-6 w-6" fill="white" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
                  </svg>
                </button>
              </div>
              )
            }


          
        </div> {/* End of: Header - mobile */}


        </div>
      </div>
    </>
  );
}
