# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import warnings
from typing import Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import grpc_helpers   # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.api_core import gapic_v1       # type: ignore
import google.auth                         # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.cloud.aiplatform_v1beta1.types import pipeline_job
from google.cloud.aiplatform_v1beta1.types import pipeline_job as gca_pipeline_job
from google.cloud.aiplatform_v1beta1.types import pipeline_service
from google.cloud.aiplatform_v1beta1.types import training_pipeline
from google.cloud.aiplatform_v1beta1.types import training_pipeline as gca_training_pipeline
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from .base import PipelineServiceTransport, DEFAULT_CLIENT_INFO


class PipelineServiceGrpcTransport(PipelineServiceTransport):
    """gRPC backend transport for PipelineService.

    A service for creating and managing Vertex AI's pipelines. This
    includes both ``TrainingPipeline`` resources (used for AutoML and
    custom training) and ``PipelineJob`` resources (used for Vertex
    Pipelines).

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """
    _stubs: Dict[str, Callable]

    def __init__(self, *,
            host: str = 'aiplatform.googleapis.com',
            credentials: ga_credentials.Credentials = None,
            credentials_file: str = None,
            scopes: Sequence[str] = None,
            channel: grpc.Channel = None,
            api_mtls_endpoint: str = None,
            client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
            ssl_channel_credentials: grpc.ChannelCredentials = None,
            client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
            quota_project_id: Optional[str] = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure mutual TLS channel. It is
                ignored if ``channel`` or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}
        self._operations_client = None

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if channel:
            # Ignore credentials if a channel was passed.
            credentials = False
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None

        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
            always_use_jwt_access=True,
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                credentials=self._credentials,
                credentials_file=credentials_file,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        # Wrap messages. This must be done after self._grpc_channel exists
        self._prep_wrapped_messages(client_info)

    @classmethod
    def create_channel(cls,
                       host: str = 'aiplatform.googleapis.com',
                       credentials: ga_credentials.Credentials = None,
                       credentials_file: str = None,
                       scopes: Optional[Sequence[str]] = None,
                       quota_project_id: Optional[str] = None,
                       **kwargs) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.

        Raises:
            google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """

        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Return the channel designed to connect to this service.
        """
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Sanity check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self._operations_client

    @property
    def create_training_pipeline(self) -> Callable[
            [pipeline_service.CreateTrainingPipelineRequest],
            gca_training_pipeline.TrainingPipeline]:
        r"""Return a callable for the create training pipeline method over gRPC.

        Creates a TrainingPipeline. A created
        TrainingPipeline right away will be attempted to be run.

        Returns:
            Callable[[~.CreateTrainingPipelineRequest],
                    ~.TrainingPipeline]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'create_training_pipeline' not in self._stubs:
            self._stubs['create_training_pipeline'] = self.grpc_channel.unary_unary(
                '/google.cloud.aiplatform.v1beta1.PipelineService/CreateTrainingPipeline',
                request_serializer=pipeline_service.CreateTrainingPipelineRequest.serialize,
                response_deserializer=gca_training_pipeline.TrainingPipeline.deserialize,
            )
        return self._stubs['create_training_pipeline']

    @property
    def get_training_pipeline(self) -> Callable[
            [pipeline_service.GetTrainingPipelineRequest],
            training_pipeline.TrainingPipeline]:
        r"""Return a callable for the get training pipeline method over gRPC.

        Gets a TrainingPipeline.

        Returns:
            Callable[[~.GetTrainingPipelineRequest],
                    ~.TrainingPipeline]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_training_pipeline' not in self._stubs:
            self._stubs['get_training_pipeline'] = self.grpc_channel.unary_unary(
                '/google.cloud.aiplatform.v1beta1.PipelineService/GetTrainingPipeline',
                request_serializer=pipeline_service.GetTrainingPipelineRequest.serialize,
                response_deserializer=training_pipeline.TrainingPipeline.deserialize,
            )
        return self._stubs['get_training_pipeline']

    @property
    def list_training_pipelines(self) -> Callable[
            [pipeline_service.ListTrainingPipelinesRequest],
            pipeline_service.ListTrainingPipelinesResponse]:
        r"""Return a callable for the list training pipelines method over gRPC.

        Lists TrainingPipelines in a Location.

        Returns:
            Callable[[~.ListTrainingPipelinesRequest],
                    ~.ListTrainingPipelinesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_training_pipelines' not in self._stubs:
            self._stubs['list_training_pipelines'] = self.grpc_channel.unary_unary(
                '/google.cloud.aiplatform.v1beta1.PipelineService/ListTrainingPipelines',
                request_serializer=pipeline_service.ListTrainingPipelinesRequest.serialize,
                response_deserializer=pipeline_service.ListTrainingPipelinesResponse.deserialize,
            )
        return self._stubs['list_training_pipelines']

    @property
    def delete_training_pipeline(self) -> Callable[
            [pipeline_service.DeleteTrainingPipelineRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the delete training pipeline method over gRPC.

        Deletes a TrainingPipeline.

        Returns:
            Callable[[~.DeleteTrainingPipelineRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'delete_training_pipeline' not in self._stubs:
            self._stubs['delete_training_pipeline'] = self.grpc_channel.unary_unary(
                '/google.cloud.aiplatform.v1beta1.PipelineService/DeleteTrainingPipeline',
                request_serializer=pipeline_service.DeleteTrainingPipelineRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['delete_training_pipeline']

    @property
    def cancel_training_pipeline(self) -> Callable[
            [pipeline_service.CancelTrainingPipelineRequest],
            empty_pb2.Empty]:
        r"""Return a callable for the cancel training pipeline method over gRPC.

        Cancels a TrainingPipeline. Starts asynchronous cancellation on
        the TrainingPipeline. The server makes a best effort to cancel
        the pipeline, but success is not guaranteed. Clients can use
        [PipelineService.GetTrainingPipeline][google.cloud.aiplatform.v1beta1.PipelineService.GetTrainingPipeline]
        or other methods to check whether the cancellation succeeded or
        whether the pipeline completed despite cancellation. On
        successful cancellation, the TrainingPipeline is not deleted;
        instead it becomes a pipeline with a
        [TrainingPipeline.error][google.cloud.aiplatform.v1beta1.TrainingPipeline.error]
        value with a [google.rpc.Status.code][google.rpc.Status.code] of
        1, corresponding to ``Code.CANCELLED``, and
        [TrainingPipeline.state][google.cloud.aiplatform.v1beta1.TrainingPipeline.state]
        is set to ``CANCELLED``.

        Returns:
            Callable[[~.CancelTrainingPipelineRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'cancel_training_pipeline' not in self._stubs:
            self._stubs['cancel_training_pipeline'] = self.grpc_channel.unary_unary(
                '/google.cloud.aiplatform.v1beta1.PipelineService/CancelTrainingPipeline',
                request_serializer=pipeline_service.CancelTrainingPipelineRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs['cancel_training_pipeline']

    @property
    def create_pipeline_job(self) -> Callable[
            [pipeline_service.CreatePipelineJobRequest],
            gca_pipeline_job.PipelineJob]:
        r"""Return a callable for the create pipeline job method over gRPC.

        Creates a PipelineJob. A PipelineJob will run
        immediately when created.

        Returns:
            Callable[[~.CreatePipelineJobRequest],
                    ~.PipelineJob]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'create_pipeline_job' not in self._stubs:
            self._stubs['create_pipeline_job'] = self.grpc_channel.unary_unary(
                '/google.cloud.aiplatform.v1beta1.PipelineService/CreatePipelineJob',
                request_serializer=pipeline_service.CreatePipelineJobRequest.serialize,
                response_deserializer=gca_pipeline_job.PipelineJob.deserialize,
            )
        return self._stubs['create_pipeline_job']

    @property
    def get_pipeline_job(self) -> Callable[
            [pipeline_service.GetPipelineJobRequest],
            pipeline_job.PipelineJob]:
        r"""Return a callable for the get pipeline job method over gRPC.

        Gets a PipelineJob.

        Returns:
            Callable[[~.GetPipelineJobRequest],
                    ~.PipelineJob]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_pipeline_job' not in self._stubs:
            self._stubs['get_pipeline_job'] = self.grpc_channel.unary_unary(
                '/google.cloud.aiplatform.v1beta1.PipelineService/GetPipelineJob',
                request_serializer=pipeline_service.GetPipelineJobRequest.serialize,
                response_deserializer=pipeline_job.PipelineJob.deserialize,
            )
        return self._stubs['get_pipeline_job']

    @property
    def list_pipeline_jobs(self) -> Callable[
            [pipeline_service.ListPipelineJobsRequest],
            pipeline_service.ListPipelineJobsResponse]:
        r"""Return a callable for the list pipeline jobs method over gRPC.

        Lists PipelineJobs in a Location.

        Returns:
            Callable[[~.ListPipelineJobsRequest],
                    ~.ListPipelineJobsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_pipeline_jobs' not in self._stubs:
            self._stubs['list_pipeline_jobs'] = self.grpc_channel.unary_unary(
                '/google.cloud.aiplatform.v1beta1.PipelineService/ListPipelineJobs',
                request_serializer=pipeline_service.ListPipelineJobsRequest.serialize,
                response_deserializer=pipeline_service.ListPipelineJobsResponse.deserialize,
            )
        return self._stubs['list_pipeline_jobs']

    @property
    def delete_pipeline_job(self) -> Callable[
            [pipeline_service.DeletePipelineJobRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the delete pipeline job method over gRPC.

        Deletes a PipelineJob.

        Returns:
            Callable[[~.DeletePipelineJobRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'delete_pipeline_job' not in self._stubs:
            self._stubs['delete_pipeline_job'] = self.grpc_channel.unary_unary(
                '/google.cloud.aiplatform.v1beta1.PipelineService/DeletePipelineJob',
                request_serializer=pipeline_service.DeletePipelineJobRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['delete_pipeline_job']

    @property
    def cancel_pipeline_job(self) -> Callable[
            [pipeline_service.CancelPipelineJobRequest],
            empty_pb2.Empty]:
        r"""Return a callable for the cancel pipeline job method over gRPC.

        Cancels a PipelineJob. Starts asynchronous cancellation on the
        PipelineJob. The server makes a best effort to cancel the
        pipeline, but success is not guaranteed. Clients can use
        [PipelineService.GetPipelineJob][google.cloud.aiplatform.v1beta1.PipelineService.GetPipelineJob]
        or other methods to check whether the cancellation succeeded or
        whether the pipeline completed despite cancellation. On
        successful cancellation, the PipelineJob is not deleted; instead
        it becomes a pipeline with a
        [PipelineJob.error][google.cloud.aiplatform.v1beta1.PipelineJob.error]
        value with a [google.rpc.Status.code][google.rpc.Status.code] of
        1, corresponding to ``Code.CANCELLED``, and
        [PipelineJob.state][google.cloud.aiplatform.v1beta1.PipelineJob.state]
        is set to ``CANCELLED``.

        Returns:
            Callable[[~.CancelPipelineJobRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'cancel_pipeline_job' not in self._stubs:
            self._stubs['cancel_pipeline_job'] = self.grpc_channel.unary_unary(
                '/google.cloud.aiplatform.v1beta1.PipelineService/CancelPipelineJob',
                request_serializer=pipeline_service.CancelPipelineJobRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs['cancel_pipeline_job']


__all__ = (
    'PipelineServiceGrpcTransport',
)