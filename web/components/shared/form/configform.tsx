'use client';
import React from 'react';
import SliderElement from '@/components/shared/form/slider';
import * as Label from '@radix-ui/react-label';
import TooltipSimple from '@/components/shared/tooltip_simple';
import CheckboxElement from '@/components/shared/form/checkbox'
import InputElement from '@/components/shared/form/input'

export interface ConfigField {
    type: string;
    label?: string | undefined;
    default: number | string | boolean | undefined;
    max?: number;
    min?: number;
    step?: number;
    tooltip?: string;
}
  
export type ConfigFields = {
    [key: string]: ConfigField;
}

export interface ConfigFormProps {
  fields: ConfigFields;
  form: {[key: string]: string | number | boolean | undefined};
}

function titleize(str: string): string {
  return str
    .split('_')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

export const ConfigForm: React.FC<ConfigFormProps> = ({ fields, form }) =>  {
    let rows: JSX.Element[] = [];
    let elements: JSX.Element[] = [];
    let counter = 0;
    const N = 4; // Replace with your desired value

    Object.entries(fields).forEach(([key, { type, label }], index) => {
      let element: JSX.Element | null;
      let tooltip = '';
      const tooltipTxt = fields[key].tooltip;
      if (tooltipTxt !== undefined) { 
        tooltip = tooltipTxt;
      }
      element = null;

      if (type == 'slider') {
        let sliderVal = '';
        if (form[key] !== undefined) {
          sliderVal = form[key]!.toString();
        }
        element = (
          <div className="flex w-1/4" key={key}>
            <SliderElement defaultValue={512} max={2048} step={1} ariaLabel={key} sliderId="tokens" />
          </div>
        );
      }
      else if (type == 'text' || type == 'int' || type == 'float') {
        let val = '';
        if (form[key] !== undefined) {
          val = form[key]!.toString();
        }
        element = (
          <div className="flex w-1/4" key={key}>
            <InputElement
              id={key}
              label={titleize(key)}
              type={type}
              defaultVal={val}
              tooltipText={tooltip}
            ></InputElement>
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
            <div className="flex w-1/4" key={key}>
              <CheckboxElement label={titleize(key)} id={key} defaultVal={booleanVariable} />
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
      else if (type == 'textarea') {
        element = (
          <div className="flex w-3/4" key={key}>
            <Label.Root className="flex w-1/6 text-[15px] font-medium leading-[35px] text-white" htmlFor="firstName">
              {label}
            </Label.Root>
            <div className="flex w-4/6">
              <textarea
                id="user-input"
                defaultValue=""
                className="form-control"
                rows={4}
                style={{ width: '100%' }}
              ></textarea>
            </div>
          </div>
        )
      } else if (type == 'spacer') { 
        element = (
          <hr></hr> 
        )
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
