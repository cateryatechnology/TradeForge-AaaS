"""
TradeForge AaaS - DeFi Service
Author: Ary HH
Email: cateryatechnology@proton.me
GitHub: https://github.com/cateryatechnology
© 2026

DeFi operations for Uniswap V3, Aave V3, and Chainlink price feeds.
"""

from typing import Optional, Dict, Any, Tuple
from decimal import Decimal
from web3 import Web3
from web3.contract import Contract
from eth_account import Account
from eth_account.signers.local import LocalAccount
import logging

from app.core.config import settings


logger = logging.getLogger(__name__)


class DeFiService:
    """
    Service for interacting with DeFi protocols.
    Supports Uniswap V3 swaps, Aave V3 lending/borrowing, and Chainlink price feeds.
    """
    
    def __init__(
        self,
        network: str = "ethereum",
        private_key: Optional[str] = None
    ):
        """
        Initialize DeFi service.
        
        Args:
            network: Blockchain network (ethereum, polygon, arbitrum)
            private_key: Wallet private key (optional)
        """
        self.network = network
        self.w3 = self._get_web3_instance(network)
        self.account: Optional[LocalAccount] = None
        
        if private_key:
            self.set_account(private_key)
        
        # Contract addresses (Ethereum Mainnet)
        self.uniswap_v3_router = settings.UNISWAP_V3_ROUTER
        self.uniswap_v3_factory = settings.UNISWAP_V3_FACTORY
        self.aave_v3_pool = settings.AAVE_V3_POOL
        self.aave_v3_data_provider = settings.AAVE_V3_POOL_DATA_PROVIDER
        
        logger.info(f"DeFi service initialized for {network}")
    
    def _get_web3_instance(self, network: str) -> Web3:
        """Get Web3 instance for specified network."""
        rpc_urls = {
            "ethereum": settings.ETH_RPC_URL,
            "polygon": settings.POLYGON_RPC_URL,
            "arbitrum": settings.ARBITRUM_RPC_URL,
        }
        
        rpc_url = rpc_urls.get(network, settings.ETH_RPC_URL)
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        
        if not w3.is_connected():
            raise ConnectionError(f"Failed to connect to {network} network")
        
        return w3
    
    def set_account(self, private_key: str) -> None:
        """
        Set wallet account from private key.
        
        Args:
            private_key: Wallet private key (with or without 0x prefix)
        """
        if not private_key.startswith("0x"):
            private_key = "0x" + private_key
        
        self.account = Account.from_key(private_key)
        logger.info(f"Account set: {self.account.address}")
    
    def get_balance(self, address: Optional[str] = None) -> Decimal:
        """
        Get ETH/native token balance.
        
        Args:
            address: Wallet address (uses account address if not provided)
        
        Returns:
            Balance in ETH/native token
        """
        addr = address or (self.account.address if self.account else None)
        
        if not addr:
            raise ValueError("No address provided and no account set")
        
        balance_wei = self.w3.eth.get_balance(addr)
        balance_eth = self.w3.from_wei(balance_wei, 'ether')
        
        return Decimal(str(balance_eth))
    
    def get_token_balance(
        self,
        token_address: str,
        wallet_address: Optional[str] = None
    ) -> Decimal:
        """
        Get ERC20 token balance.
        
        Args:
            token_address: Token contract address
            wallet_address: Wallet address (uses account address if not provided)
        
        Returns:
            Token balance
        """
        addr = wallet_address or (self.account.address if self.account else None)
        
        if not addr:
            raise ValueError("No address provided and no account set")
        
        # ERC20 ABI (minimal)
        erc20_abi = [
            {
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [],
                "name": "decimals",
                "outputs": [{"name": "", "type": "uint8"}],
                "type": "function"
            }
        ]
        
        token_contract = self.w3.eth.contract(
            address=self.w3.to_checksum_address(token_address),
            abi=erc20_abi
        )
        
        balance = token_contract.functions.balanceOf(addr).call()
        decimals = token_contract.functions.decimals().call()
        
        return Decimal(balance) / Decimal(10 ** decimals)
    
    async def swap_uniswap_v3(
        self,
        token_in: str,
        token_out: str,
        amount_in: Decimal,
        slippage_tolerance: float = 0.5,
        fee_tier: int = 3000
    ) -> Dict[str, Any]:
        """
        Swap tokens on Uniswap V3.
        
        Args:
            token_in: Input token address
            token_out: Output token address
            amount_in: Amount of input token
            slippage_tolerance: Slippage tolerance in percent (default 0.5%)
            fee_tier: Pool fee tier (500, 3000, or 10000)
        
        Returns:
            Transaction details
        """
        if not self.account:
            raise ValueError("No account set. Call set_account() first.")
        
        try:
            # This is a simplified example. In production, use web3-ethereum-defi
            # or uniswap-python library for proper swap execution
            
            logger.info(
                f"Swapping {amount_in} of {token_in} for {token_out} "
                f"with {slippage_tolerance}% slippage on Uniswap V3"
            )
            
            # Calculate minimum amount out based on slippage
            # In production, get quote from Uniswap quoter contract
            min_amount_out = amount_in * Decimal(1 - slippage_tolerance / 100)
            
            # Prepare swap parameters
            swap_params = {
                "tokenIn": token_in,
                "tokenOut": token_out,
                "fee": fee_tier,
                "recipient": self.account.address,
                "deadline": self.w3.eth.get_block('latest')['timestamp'] + 300,  # 5 min
                "amountIn": int(amount_in * Decimal(10**18)),
                "amountOutMinimum": int(min_amount_out * Decimal(10**18)),
                "sqrtPriceLimitX96": 0
            }
            
            # TODO: Implement actual swap using Uniswap V3 router
            # This would require:
            # 1. Approve token_in for router
            # 2. Call exactInputSingle on router
            # 3. Sign and send transaction
            
            return {
                "status": "simulated",
                "swap_params": swap_params,
                "estimated_output": float(min_amount_out),
                "note": "This is a simulation. Implement actual swap in production."
            }
            
        except Exception as e:
            logger.error(f"Swap failed: {str(e)}")
            raise
    
    async def deposit_aave_v3(
        self,
        asset: str,
        amount: Decimal,
        on_behalf_of: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Deposit (lend) asset to Aave V3.
        
        Args:
            asset: Asset token address
            amount: Amount to deposit
            on_behalf_of: Address to deposit on behalf of (defaults to account)
        
        Returns:
            Transaction details
        """
        if not self.account:
            raise ValueError("No account set. Call set_account() first.")
        
        try:
            recipient = on_behalf_of or self.account.address
            
            logger.info(
                f"Depositing {amount} of {asset} to Aave V3 "
                f"on behalf of {recipient}"
            )
            
            # Aave V3 Pool minimal ABI
            pool_abi = [
                {
                    "inputs": [
                        {"internalType": "address", "name": "asset", "type": "address"},
                        {"internalType": "uint256", "name": "amount", "type": "uint256"},
                        {"internalType": "address", "name": "onBehalfOf", "type": "address"},
                        {"internalType": "uint16", "name": "referralCode", "type": "uint16"}
                    ],
                    "name": "supply",
                    "outputs": [],
                    "stateMutability": "nonpayable",
                    "type": "function"
                }
            ]
            
            pool_contract = self.w3.eth.contract(
                address=self.w3.to_checksum_address(self.aave_v3_pool),
                abi=pool_abi
            )
            
            amount_wei = int(amount * Decimal(10**18))
            
            # TODO: Implement actual deposit
            # This would require:
            # 1. Approve asset for Aave pool
            # 2. Call supply on pool
            # 3. Sign and send transaction
            
            return {
                "status": "simulated",
                "asset": asset,
                "amount": float(amount),
                "recipient": recipient,
                "note": "This is a simulation. Implement actual deposit in production."
            }
            
        except Exception as e:
            logger.error(f"Deposit failed: {str(e)}")
            raise
    
    async def borrow_aave_v3(
        self,
        asset: str,
        amount: Decimal,
        interest_rate_mode: int = 2,  # 1 = stable, 2 = variable
        on_behalf_of: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Borrow asset from Aave V3.
        
        Args:
            asset: Asset token address
            amount: Amount to borrow
            interest_rate_mode: 1 for stable, 2 for variable
            on_behalf_of: Address to borrow on behalf of (defaults to account)
        
        Returns:
            Transaction details
        """
        if not self.account:
            raise ValueError("No account set. Call set_account() first.")
        
        try:
            recipient = on_behalf_of or self.account.address
            
            logger.info(
                f"Borrowing {amount} of {asset} from Aave V3 "
                f"(rate mode: {interest_rate_mode})"
            )
            
            # TODO: Implement actual borrow
            # Check health factor before borrowing
            # Call borrow on Aave pool
            
            return {
                "status": "simulated",
                "asset": asset,
                "amount": float(amount),
                "interest_rate_mode": "variable" if interest_rate_mode == 2 else "stable",
                "note": "This is a simulation. Implement actual borrow in production."
            }
            
        except Exception as e:
            logger.error(f"Borrow failed: {str(e)}")
            raise
    
    async def repay_aave_v3(
        self,
        asset: str,
        amount: Decimal,
        interest_rate_mode: int = 2,
        on_behalf_of: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Repay borrowed asset to Aave V3.
        
        Args:
            asset: Asset token address
            amount: Amount to repay (use max uint256 for full repayment)
            interest_rate_mode: 1 for stable, 2 for variable
            on_behalf_of: Address to repay on behalf of (defaults to account)
        
        Returns:
            Transaction details
        """
        if not self.account:
            raise ValueError("No account set. Call set_account() first.")
        
        try:
            recipient = on_behalf_of or self.account.address
            
            logger.info(
                f"Repaying {amount} of {asset} to Aave V3"
            )
            
            # TODO: Implement actual repay
            # Approve asset for Aave pool
            # Call repay on Aave pool
            
            return {
                "status": "simulated",
                "asset": asset,
                "amount": float(amount),
                "note": "This is a simulation. Implement actual repay in production."
            }
            
        except Exception as e:
            logger.error(f"Repay failed: {str(e)}")
            raise
    
    def get_chainlink_price(self, feed_address: str) -> Tuple[Decimal, int]:
        """
        Get latest price from Chainlink price feed.
        
        Args:
            feed_address: Chainlink price feed address
        
        Returns:
            Tuple of (price, decimals)
        """
        # Chainlink AggregatorV3Interface ABI (minimal)
        aggregator_abi = [
            {
                "inputs": [],
                "name": "latestRoundData",
                "outputs": [
                    {"internalType": "uint80", "name": "roundId", "type": "uint80"},
                    {"internalType": "int256", "name": "answer", "type": "int256"},
                    {"internalType": "uint256", "name": "startedAt", "type": "uint256"},
                    {"internalType": "uint256", "name": "updatedAt", "type": "uint256"},
                    {"internalType": "uint80", "name": "answeredInRound", "type": "uint80"}
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function"
            }
        ]
        
        feed_contract = self.w3.eth.contract(
            address=self.w3.to_checksum_address(feed_address),
            abi=aggregator_abi
        )
        
        # Get latest price
        round_data = feed_contract.functions.latestRoundData().call()
        price_raw = round_data[1]  # answer
        
        # Get decimals
        decimals = feed_contract.functions.decimals().call()
        
        # Convert to decimal
        price = Decimal(price_raw) / Decimal(10 ** decimals)
        
        return price, decimals
    
    def get_eth_usd_price(self) -> Decimal:
        """Get ETH/USD price from Chainlink."""
        price, _ = self.get_chainlink_price(settings.CHAINLINK_ETH_USD)
        return price
    
    def get_btc_usd_price(self) -> Decimal:
        """Get BTC/USD price from Chainlink."""
        price, _ = self.get_chainlink_price(settings.CHAINLINK_BTC_USD)
        return price


# Export for convenience
__all__ = ["DeFiService"]
