from loguru import logger

class StandardAuthBackend: 
    async def validate(self, username, password):
        if await self.validate_impl(username, password):
            logger.info(f"Successfully authenticated the user {username}")
        else:
            logger.info(f"Could not authenticate the user {username}")
    
    async def validate_impl(self, username, password):
        raise NotImplementedError("Validate needs to be overridden")