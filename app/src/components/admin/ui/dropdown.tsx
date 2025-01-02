import * as React from "react";
import { useState } from "react";

export interface DropdownProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  options: { value: number; label: string }[];
  placeHolder: string;
}

const Dropdown = React.forwardRef<HTMLSelectElement, DropdownProps>(
  ({ className, options, placeHolder, value, disabled, ...props }, ref) => {

    const [selectedOption, setSelectedOption] = useState(value || "");

    React.useEffect(() => {
      if (value !== undefined) {
        setSelectedOption(value);
      }
    }, [value]);


    const handleSelectChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
      setSelectedOption(event.target.value);
      if (props.onChange) props.onChange(event);
    };

    return (
      <>
      <div className="relative w-full">
        <select
        disabled={disabled}
          value={selectedOption}
          onChange={handleSelectChange}
          className={`
            "flex h-9 w-full rounded-md border border-input px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50",
            ${className || ''}`
          }
          // ref={ref}
          // {...props}
        >
          <option value="" disabled>
            {placeHolder}
          </option>
          {options.map((option, index) => (
            <option key={index} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>
      </>
    );
  }
);

Dropdown.displayName = "Dropdown";

export { Dropdown };
