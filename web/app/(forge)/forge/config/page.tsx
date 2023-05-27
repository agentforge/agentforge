'use client';
import { v4 as uuidv4 } from 'uuid';
import React, { useEffect, useRef, useState, KeyboardEvent } from 'react';
import { ReflectionProps } from '@/components/shared/reflection';
import { useLanguageModelConfig } from '@/components/shared/context/languagemodelconfigcontext';
import ChatWidget from '@/components/shared/chatwidget';
import MainConfigForm from './mainconfig';

interface ConfigProps {}

const Config: React.FC<ConfigProps> = () => {

  return (
    <>
    <div className="md:block w-full h-full md:w-8/12">
        <MainConfigForm/>
    </div>
    </>
)};

export default Config;