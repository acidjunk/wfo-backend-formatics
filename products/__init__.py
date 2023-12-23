# Copyright 2019-2023 SURF.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from orchestrator.domain import SUBSCRIPTION_MODEL_REGISTRY

from products.product_types.email import Email

SUBSCRIPTION_MODEL_REGISTRY.update(
    {
        "Marketing email": Email,
        "Reminder email": Email,
        "Reactivation email": Email,
        "Platform email": Email,
        }
)  # fmt:skip
