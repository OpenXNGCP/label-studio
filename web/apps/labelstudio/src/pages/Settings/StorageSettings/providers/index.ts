import azureProvider from "./azure";
import azureSpiProvider from "./azure_spi";
import databricksProvider from "./databricks";
import gcsProvider from "./gcs";
import gcsWifProvider from "./gcswif";
import localFilesProvider from "./localFiles";
import redisProvider from "./redis";
import { s3Provider } from "./s3";
import oss2Provider from "./oss2";
import s3sProvider from "./s3s";

  // Standard providers
  s3: s3Provider,
  gcs: gcsProvider,
  azure: azureProvider,
  redis: redisProvider,
  oss2: oss2Provider,
  // Enterprise providers
  databricks: databricksProvider,
  s3s: s3sProvider,
  gcswif: gcsWifProvider,
  azure_spi: azureSpiProvider,
  // Local provider
  localfiles: localFilesProvider,
};
