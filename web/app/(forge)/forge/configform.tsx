'use client';
import React from 'react';
import { Checkbox, Spacer } from '@nextui-org/react';
import SliderElement from '@/components/shared/slider';
import * as Label from '@radix-ui/react-label';
import TooltipSimple from '@/components/shared/tooltip_simple';

interface ConfigField {
    type: string;
    default: number | string | boolean | undefined;
    max?: number;
    min?: number;
    step?: number;
    tooltip?: string;
}
  
type ConfigFields = {
    [key: string]: ConfigField;
}

interface ConfigFormProps {
  fields: ConfigFields;
  form: {[key: string]: string | number | boolean | undefined};
}

const ConfigForm: React.FC<ConfigFormProps> = ({ fields, form }) =>  {
    let rows: JSX.Element[] = [];
    let elements: JSX.Element[] = [];
    let counter = 0;
    const N = 4; // Replace with your desired value

    Object.entries(fields).forEach(([key, { type }], index) => {
      let element: JSX.Element | null;
      element = null;

      if (type == 'slider') {
        let sliderVal = '';
        if (form[key] !== undefined) {
          sliderVal = form[key]!.toString();
        }
        element = (
          <div className="flex w-1/4">
            <SliderElement defaultValue={512} max={2048} step={1} ariaLabel={key} sliderId="tokens" />
            <Spacer y={2.5} />
          </div>
        );
      }
      else if (type == 'text' || type == 'number') {

        let val = '';
        if (form[key] !== undefined) {
          val = form[key]!.toString();
        }
        element = (
          <div className="flex w-1/4">
            <div className="flex flex-wrap items-center gap-[15px] px-5">
              <Label.Root className="text-[15px] font-medium leading-[35px] text-white" htmlFor={ key }>
                {key}
                {fields[key].tooltip !== undefined ? (
                  <TooltipSimple text={fields[key].tooltip} /> 
                ) : (       
                  <></>
                )}
              </Label.Root>
              <input
                className="bg-blackA5 shadow-blackA9 inline-flex h-[35px] w-full appearance-none items-center justify-center rounded-[4px] px-[10px] text-[15px] leading-none text-white shadow-[0_0_0_1px] outline-none focus:shadow-[0_0_0_2px_black] selection:color-white selection:bg-blackA9"
                type={ type }
                id={ key }
                defaultValue={ val }
              />
            </div>
            {/* <Input bordered key={key} labelPlaceholder={key} type="number" />
            <Spacer y={2.5} /> */}
          </div>
        );
       }
       else if (type == 'boolean') { 

        // Handle typesafety
        let variable: string | number | boolean | undefined = form[key];
        let booleanVariable: boolean | undefined;
        if (typeof variable === 'boolean' || typeof variable === 'undefined') {
          booleanVariable = variable;
          element = (
            <div className="flex w-1/4">
              <Checkbox key={key} label={key} name={key} />
              {fields[key].tooltip !== undefined ? (
                  <TooltipSimple text={fields[key].tooltip} /> 
                ) : (       
                  <></>
              )}
            </div>
          );
        } else {
          element = <span>Error incorrect type</span>;
        }
      }
      if (element) {
        elements.push(element);
        counter++;
        if (counter === N || index === Object.keys(fields).length - 1) {
          rows.push(<div className="flex flex-row mt-9" key={`row${index}`}>{elements}</div>);
          elements = [];
          counter = 0;
        }
      }
    });

    return (
      <>
          {rows}
      </>
  );
}

export default ConfigForm;
