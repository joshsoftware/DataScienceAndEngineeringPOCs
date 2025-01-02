'use client'

import { Button } from "./ui/button";
import { Card, CardContent, CardFooter } from "./ui/card";
import { toast } from "sonner";
import { Fragment, useState } from "react";

const EmbeddedCodeCard = () => {
  const [copyButtonText, setCopyButtonText] = useState("Copy to clipboard");
  const code = `<!DOCTYPE html>
<html>
<head>
<title>Page Title</title>
</head>
<body>

<h1>This is a Heading</h1>
<p>This is a paragraph.</p>

</body>

</html>`

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopyButtonText("Copied to clipboard");
      toast.success("Copied to clipboard!");
    } catch (err) {
      toast.error("Failed to copy!");
    }
  };
  return (

    <div className="flex flex-col justify-between w-full items-center">
      <Card className="bg-[#fafbff] w-2/4">
        <CardContent className="flex-grow pt-2">
          <pre>
            <code>
              {code}
            </code>
          </pre>

        </CardContent>
      </Card>

      <CardFooter>
        <div className="flex flex-col justify-center items-center w-full md:flex-row gap-4 pt-4">
          {(
            <Fragment>
              <Button
                onClick={(e) => {
                  e.stopPropagation();
                  handleCopy();
                }}
                // disabled={isTextPresent}
                className="flex bg-[#668D7E] hover:bg-[#668D7E] text-white w-full"
              >
                {copyButtonText}
              </Button>
            </Fragment>
          )}
        </div>
      </CardFooter>
    </div>
  )
}

export default EmbeddedCodeCard;
