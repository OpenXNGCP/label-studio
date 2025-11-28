import { z } from "zod";
import type { ProviderConfig } from "@humansignal/app-common/blocks/StorageProviderForm/types/provider";
import { IconCloudProviderS3 } from "@humansignal/icons";

export const oss2Provider: ProviderConfig = {
  name: "oss2",
  title: "Alibaba Cloud OSS",
  description: "Configure your Alibaba Cloud OSS connection for Label Studio.",
  icon: IconCloudProviderS3, // Replace with OSS icon if available
  fields: [
    {
      name: "bucket",
      type: "text",
      label: "Bucket Name",
      required: true,
      placeholder: "my-oss-bucket",
      schema: z.string().min(1, "Bucket name is required"),
    },
    {
      name: "endpoint",
      type: "text",
      label: "OSS Endpoint",
      required: true,
      placeholder: "https://oss-cn-hangzhou.aliyuncs.com",
      schema: z.string().min(1, "Endpoint is required"),
    },
    {
      name: "oss_access_key_id",
      type: "text",
      label: "Access Key ID",
      required: true,
      placeholder: "LTAI...",
      schema: z.string().min(1, "Access Key ID is required"),
    },
    {
      name: "oss_access_key_secret",
      type: "password",
      label: "Access Key Secret",
      required: true,
      placeholder: "Your secret...",
      schema: z.string().min(1, "Access Key Secret is required"),
    },
    {
      name: "prefix",
      type: "text",
      label: "Bucket Prefix",
      placeholder: "path/to/files",
      schema: z.string().optional().default("")
    },
    {
      name: "regex_filter",
      type: "text",
      label: "Regex Filter",
      placeholder: "^.*\\.json$",
      schema: z.string().optional().default("")
    },
    {
      name: "use_blob_urls",
      type: "checkbox",
      label: "Use Blob URLs",
      schema: z.boolean().optional().default(false),
    },
  ],
};

export default oss2Provider;
