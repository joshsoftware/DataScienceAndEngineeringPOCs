'use client'

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { configuratorRequest, configuratorSchema } from "@/Validators/configurator";
import { Dropdown } from "./ui/dropdown";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { Card, CardContent } from "./ui/card";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/admin/ui/form";
import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import { toast } from "sonner";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

const ConfiguratorForm = () => {

  const [disableFields, setDisableFields] = useState(false);
  const [editConf, setEditConfiguration] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isDataPResent, setIsDataPResent] = useState(false);

  useEffect(() => {
  const adminEmail = localStorage.getItem("email")
  if(adminEmail) {
    const emailDomain = adminEmail.substring(adminEmail.indexOf('@') + 1);
    getConfiguratorData(emailDomain);
  }

  }, [])
  const router = useRouter()

  const form = useForm<configuratorRequest>({
    resolver: zodResolver(configuratorSchema),
    defaultValues: {
      url: "",
    },
    mode: "all",
  });

  const { handleSubmit, setValue } = form;

  const options = [
    { value: 1, label: "1" },
    { value: 2, label: "2" },
    { value: 3, label: "3" },
  ];

  const frequencies = [
    { value: 5, label: "5 Days" },
    { value: 15, label: "15 Days" },
    { value: 30, label: "30 Days" },
  ];

  const handleSelectDepth = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setValue("depth", parseInt(event.target.value, 10));
  };

  const handleSelectPages = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setValue("maxPages", parseInt(event.target.value, 10));
  };

  const handleSelectFrequency = (event: any) => {
    const selectedFrequency = parseInt(event.target.value, 10);
    setValue("frequency", selectedFrequency);
  };

  const onSubmit = async (data: configuratorRequest) => {
    if (editConf) {
      editConfiguratorData(data);
    } else {
      SaveConfiguratorData(data);
    }
  };

  const redirect = () => {
    router.push("/admin/embeddedCode")
  }

  const editConfiguration = (isEdit: boolean = false) => {
    setDisableFields(!isEdit)
    setEditConfiguration(isEdit);
  }

  const { mutate: SaveConfiguratorData } = useMutation({
    mutationKey: ["configurator"],
    mutationFn: async (data: configuratorRequest) => {
      const website = new URL(data.url);
      setIsLoading(true);
      data.domain = (website.hostname).replace(/^www\./, '');
      const response = await axios.post("/admin/api/configurator/save", data);
      return response;
    },
    onSuccess: async (response: any) => {
      const { data, status } = response;
      if (status == 200) {
        setIsLoading(false);
        toast.success(data);
        router.push("/admin/embeddedCode")
        form.reset();
      } else {
        setIsLoading(false);
        toast.error(data);
        form.reset();
      }
    },
    onError: (error) => {
      setIsLoading(false);
      return toast.error(error?.message ??
        "Failed to save Configurator, please try again in some time"
      );
    },
  });

  const { mutate: editConfiguratorData } = useMutation({
    mutationKey: ["editConfiguratorData"],
    mutationFn: async (data: configuratorRequest) => {
      const website = new URL(data.url);
      setIsLoading(true);
      data.domain = (website.hostname).replace(/^www\./, '');
      const response = await axios.post("/admin/api/configurator/edit", data);
      return response;
    },
    onSuccess: async (response: any) => {
      const { data, status } = response;
      if (status == 200) {
        setIsLoading(false);
        toast.success(data);
        router.push("/admin/embeddedCode")
        form.reset();
      } else {
        setIsLoading(false);
        toast.error(data);
        form.reset();
      }
    },
    onError: (error) => {
      setIsLoading(false);
      return toast.error(error?.message ??
        "Failed to save Configurator, please try again in some time"
      );
    },
  });
  const { mutate: getConfiguratorData } = useMutation({
    mutationKey: ["getConfigurator"],
    mutationFn: async (domain: string) => {

      const response = await axios.post("/admin/api/configurator/get", { domain });
      return response;
    },
    onSuccess: async (response: any) => {
      const { data } = response;
      if (data.data) {
        setDisableFields(true);
        setIsDataPResent(true);
        setValue("depth", parseInt(data.data.websiteDepth));
        setValue("maxPages", parseInt(data.data.websiteMaxNumberOfPages));
        setValue("frequency", parseInt(data.data.websiteFrequency));
        setValue("url", data.data.websiteUrl);
      } else {
        setDisableFields(false);
        setIsDataPResent(false);
      }
    },
    onError: (error) => {
     // code
    },
  });

  return (
    <div className="flex flex-col gap-2 w-full justify-center items-center">
      <div className="flex flex-1 justify-center items-start w-2/4">
        <Card className="bg-[#fafbff] flex flex-col justify-between w-full h-full items-center">
          <CardContent className="flex-grow pt-2 w-3/5">
            <Form {...form}>
              <form
                onSubmit={handleSubmit(onSubmit)}
                className="w-full max-w-sm flex flex-col gap-4 justify-center items-center"
              >
                <h1 className="text-3xl font-bold">Website Configuration</h1>

                <div className="grid w-full max-w-sm items-center gap-1.5">
                  <FormField
                    control={form.control}
                    name="url"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Website URL</FormLabel>
                        <FormControl>
                          <Input disabled={disableFields} {...field} placeholder="Enter your website URL" />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>

                <div className="grid w-full max-w-sm items-center gap-1.5">
                  <FormField
                    control={form.control}
                    name="depth"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Max Pages</FormLabel>
                        <FormControl>
                          <Dropdown
                            disabled={disableFields}
                            value={field.value}
                            options={options}
                            placeHolder="Enter Max Pages"
                            onChange={handleSelectPages}
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>

                <div className="grid w-full max-w-sm items-center gap-1.5">
                  <FormField
                    control={form.control}
                    name="depth"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Depth Level</FormLabel>
                        <FormControl>
                          <Dropdown
                            disabled={disableFields}
                            value={field.value}
                            options={options}
                            placeHolder="Select Depth"
                            onChange={handleSelectDepth}
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>

                <div className="grid w-full max-w-sm items-center gap-1.5">
                  <FormField
                    control={form.control}
                    name="frequency"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>frequency</FormLabel>
                        <FormControl>
                          <Dropdown
                            disabled={disableFields}
                            value={field.value}
                            options={frequencies}
                            placeHolder="Select Frequency"
                            onChange={handleSelectFrequency}
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>
                {
                  disableFields ?
                    <div className="w-full">
                      <div className="flex flex-1 gap-2 justify-center items-start">
                        <button type="button" onClick={() => editConfiguration(true)} className=" bg-transparent  border border-[#668D7E]-500 rounded-md text-sm font-medium  disabled:opacity-50 bg-[#668D7E] hover:bg-[#668D7E]  text-black hover:text-white w-full h-10 py-2 px-">
                          Edit</button>
                        <button type="button" onClick={() => redirect()} className=" rounded-md text-sm font-medium  disabled:opacity-50 bg-[#668D7E] hover:bg-[#668D7E] text-white w-full h-10 py-2 px-">
                          Show widget</button>
                      </div>
                    </div>

                    :
                    <div className="w-full">
                    <div className="flex flex-1 gap-2 justify-center items-start">
                      {isDataPResent && <button type="button" onClick={() => editConfiguration(false)} className=" bg-transparent  border border-[#668D7E]-500 rounded-md text-sm font-medium  disabled:opacity-50 bg-[#668D7E] hover:bg-[#668D7E]  text-black hover:text-white w-full h-10 py-2 px-">
                        Cancel</button> }
                        <Button isLoading={isLoading} type="submit" className="bg-[#668D7E] hover:bg-[#668D7E] text-white w-full">
                      Submit
                    </Button>
                    </div>
                  </div>
                }
              </form>
            </Form>
          </CardContent>
        </Card>
      </div>
    </div >
  );
};

export default ConfiguratorForm;
