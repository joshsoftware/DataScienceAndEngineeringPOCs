import * as React from "react";
import { useState } from "react";
import { EyeIcon, EyeOffIcon } from "lucide-react";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

const Input = React.forwardRef<HTMLInputElement, InputProps>(({ className, type, disabled, ...props }, ref) => {
  const [showPassword, setShowPassword] = useState(false);

  const togglePasswordVisibility = () => {
    setShowPassword((prev) => !prev);
  };

  return (
    <div className="relative w-full">
      <input 
      disabled={disabled}
        type={type === "password" && showPassword ? "text" : type}
        className={`
          flex h-9 w-full rounded-md border border-input px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50
          ${className || ''}`
        }
        ref={ref}
        {...props}
      />
      {type === "password" && (
        <button
          type="button"
          onClick={togglePasswordVisibility}
          className="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-500"
        >
          {showPassword ? <EyeIcon className="h-5 w-5" /> : <EyeOffIcon className="h-5 w-5" />}
        </button>
      )}
    </div>
  );
});

Input.displayName = "Input";

export { Input };